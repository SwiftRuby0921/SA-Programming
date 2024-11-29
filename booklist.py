#! /usr/bin/env python3
import sys
import os
import io
import cgi
import urllib.parse
import sqlite3


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

form = {} # 辞書を初期化

content_length = os.environ.get('CONTENT_LENGTH') # 入力データ長を取得
if content_length: # 入力データがある場合
  body = sys.stdin.read(int(content_length)) # 入力データを標準入力から読み込み
  params = body.split('&') # 入力データを & で分割
  for param in params: # 分割されたデータを順に処理
    key, value = param.split('=') # 分割データを = で分割
    # form[key] = urllib.parse.unquote(value) #   キーと値を辞書に登録（値はURLデコードする）
    form[key] = urllib.parse.unquote_plus(value) # httpで空白を入れると、+に変換されたので、unquote_plusでplusを空白に戻す

    
param_str = form['param1']# ブラウザから送信されたparam1の値を辞書から取得

db_path = "bookdb.db"			# データベースファイル名を指定

con = sqlite3.connect(db_path)	# データベースに接続
con.row_factory = sqlite3.Row	# 属性名で値を取り出せるようにする
cur = con.cursor()				# カーソルを取得





print("Content-type: text/html")
print("")
print("<html>")
print(""" <head>
      <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/> """)
      # </head>""")
      # <title> Search_Result</title>
print("""
   <script>
        let priceAscending = true;
        let publisherAscending = true;
        function sortPrice() {
            const table = document.getElementById("resultsTable");
            const rows = Array.from(table.rows).slice(1); // 첫 번째 행(헤더)을 제외한 나머지 행 가져오기

            rows.sort((a, b) => {
                const priceA = parseFloat(a.cells[4].textContent);
                const priceB = parseFloat(b.cells[4].textContent);

                return priceAscending ? priceA - priceB : priceB - priceA; // 오름차순 또는 내림차순 정렬
            });

            // 정렬된 행 다시 추가
            rows.forEach(row => table.appendChild(row));
            priceAscending = !priceAscending; // 정렬 순서 반전
        }
        
        function sortPublisher() {
            const table = document.getElementById("resultsTable");
            const rows = Array.from(table.rows).slice(1); // 첫 번째 행(헤더)을 제외한 나머지 행 가져오기

            rows.sort((a, b) => {
                const publisherA = a.cells[3].textContent.toLowerCase();
                const publisherB = b.cells[3].textContent.toLowerCase();

             return publisherAscending ? publisherA.localeCompare(publisherB) : publisherB.localeCompare(publisherA); // 내림차순 정렬
            });

            // 정렬된 행 다시 추가
            rows.forEach(row => table.appendChild(row));
            publisherAscending = !publisherAscending; // 정렬 순서 반전
        }
  
    </script>
    """)
    
print("</head>")
print(" <style> body {background-color:rgb(249, 226, 204); }")
# print("<table> {border: 1px; width: 100%;>} ")
print("table { width: 100%; border-collapse: collapse; margin: 20px 0; }")
print("th {background-color: rgb(74, 165, 221); text-align: center;}")
print("th{cursor: pointer; scope : col}")
print("tr{ background-color: rgb(160, 207, 237); text-align : center;}") #結果の表の色

print("</style>")
#html Body
#efc384
print("<body>")
print(f"<h1 style=\"text-align: center;\">\"{param_str}\"の検索結果一覧</h1>")

multiple_param = []
multiple_param = param_str.split()

query1 = "select * from BOOKLIST where"
subquery = []
var1 = []   

for param in multiple_param:
  # subquery.append("TITLE like ? or AUTHOR like ?")
  query1 += "(TITLE like ? or AUTHOR like ?) AND"
  var1.extend(["%" + param + "%", "%" + param+ "%"])

query1 =query1[:-3]

# query = "select * from BOOKLIST where TITLE like ? or AUTHOR like ?"
# if len(multiple_param) <= 1:
#   cur.execute("select * from BOOKLIST where TITLE like ? or AUTHOR like ?", ('%' + param_str + '%', '%' + param_str + '%',))
# else:
#   # query = "select * from BOOKLIST where "
#   # query = ""
#   # var = []
#   # for param in multiple_param:
#   #   query += "in (select * from BOOKLIST where TITLE like ? or AUTHOR like ?"
#   #   var.append("%" + param + "%")
#   #   # query += "%"+ param +"%"
#   # for param in multiple_param:
#   #   query += ")"
#   # query +=")"
#   # cur.execute(query, var)
#   # 서브쿼리 구성
#   query = "SELECT * FROM BOOKLIST WHERE TITLE LIKE ? OR AUTHOR LIKE ?"
subqueries = []
var = []
  
for param in multiple_param:
    subqueries.append("(TITLE LIKE ? OR AUTHOR LIKE ?)")
    var.extend(["%" + param + "%", "%" + param + "%"])  # TITLE과 AUTHOR에 대해 조건 추가

# 최종 쿼리 생성
query = "SELECT * FROM BOOKLIST WHERE " + " AND ".join(subqueries)

  # 쿼리 실행
cur = con.cursor()
cur.execute(query, var)
cur.execute(query1, var1)
# cur.execute("select * from BOOKLIST where TITLE like ? or AUTHOR like ?", ('%' + query + '%', '%' + query + '%',))

print(f"<h1 style=\"text-align: center;\">\"{query1}\"の検索結果一覧</h1>")
print(f"<h1 style=\"text-align: center;\">\"{query}\"の検索結果一覧</h1>")

print(f"<h1 style=\"text-align: center;\">\"{var}\"の検索結果一覧</h1>")
print(f"<h1 style=\"text-align: center;\">\"{var1}\"の検索結果一覧</h1>")
# try:
  # SQL文の実行
# cur.execute("select * from BOOKLIST where TITLE like ? or AUTHOR like ?", ('%' + param_str + '%', '%' + param_str + '%',))

rows = cur.fetchall()   # 検索結果をリストとして取得print(rows)

if not rows:        # リストが空のとき
  print("該当するデータがありません。")
else:
  # print("""<table
  #       border="1" 
  #       width="100%"
  #       > """)
        # height="200"
        # cellspacing="5">>""")
  
  # print("<tr>")
  # print("<tr bgcolor=\"#4aa5dd\" align =\"center\">")
  # print(f"<th scope = \"col\"> id</td>")
  # print(f"<th scope = \"col\"> タイトル</td>")
  # print(f"<th scope = \"col\"> 著者 </td>")
  # print(f"<th scope = \"col\"> 出版社</td>")
  # # print(f"<th scope = \"col\" onclick = \"return sort-price()\" style  =\"cursor: pointer;\">価格 </td>")
  # # print(f"<th scope = \"col\" onclick = \"return hello()\" style  =\"cursor: pointer;\">価格 </td>")
  # print(f"<th scope = \"col\" onclick = \"sort-price()\" style  =\"cursor: pointer;\">価格 </td>")
  # print(f"<th scope = \"col\"> ISBN </td>")
  # print("</tr>")
  # for row in rows:    # 検索結果を1つずつ処理
  #   print("<tr>")
  #   print("<tr bgcolor=\"#a0cfed\" align =\"center\">")
  #   print(f"<td>{row['ID']}</td>" )
  #   print(f"<td> {row['TITLE']}</td>")
  #   print(f"<td>{row['AUTHOR']}</td>")
  #   print(f"<td>{row['PUBLISHER']}</td>")
  #   print(f"<td>{row['PRICE']}</td>")
  #   print(f"<td>{row['ISBN']}</td>")
  #   print("</tr>")
  print("""
         <table id="resultsTable" border="1">
            <tr>
                <th>ID</th>
                <th>タイトル</th>
                <th>著者</th>
                <th onclick = "sortPublisher()"> 出版社</th>
                <th onclick="sortPrice()">価格</th>
                <th>ISBN</th>
            </tr>
        """)
  for row in rows:
    print("<tr>")
    
    print(f"<td>{row['ID']}</td>" )
    print(f"<td> {row['TITLE']}</td>")
    print(f"<td>{row['AUTHOR']}</td>")
    print(f"<td>{row['PUBLISHER']}</td>")
    print(f"<td>{row['PRICE']}</td>")
    print(f"<td>{row['ISBN']}</td>")
    print("</tr>")
            # <tr bgcolor=\"#a0cfed\" align =\"center\">
            # print(f"""
            # <tr>
            #     <td>{row['ID']}</td>
            #     <td>{row['TITLE']}</td>
            #     <td>{row['AUTHOR']}</td>
            #     <td>{row['PUBLISHER']}</td>
            #     <td>{row['PRICE']}</td>
            #     <td>{row['ISBN']}</td>
            # </tr>
            # """)
print("</table>")
print("""
</body>
</html>
""")
# print("""
#     </table>
#     <script>
#       function sortPrice(table, ascending){
#         if(!ascending){ 
#           table.sort((a, b) => a[4] - b[4]);
#           ascending = false;
#         }
#         else
#           table.sort((a, b) >= b[4] - a[4]);
#           ascending = true;
#       }
#     </script>
# print(" </body>")
# print("</html>")
# except sqlite3.Error as e:    # エラー処理
  # print("Error occurred:", e.args[0])
# https://wepplication.github.io/tools/colorPicker/