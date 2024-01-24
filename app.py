from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'shop'
mysql = MySQL(app)

CORS(app)

@app.route('/')
def main():
    return "Welcome"

@app.route('/shop', methods=['GET', 'POST'])
def rempah():
# Read
    if request.method == 'GET':
        try:
            # koneksi mysql
            cur = mysql.connection.cursor()
            # query untuk mengambil semua data dalam tabel
            cur.execute("SELECT * FROM my_shop")
            # fetchall mengambil semua data yang telah di query di atas, 
            # dan menyimpannya ke result
            result = cur.fetchall()
            # mengambil nama kolom dari tabel yang di query diatas (rempah)
            column_names = [i[0] for i in cur.description]
            
            # untuk membuat struktur dictionary dengan key dan value, 
            # karna result diatas hanya berupa json value tanpa ada key
            data = []
            for row in result:
                data.append(dict(zip(column_names, row)))
            
            # menutup koneksi
            cur.close()
            
            # mengembalikan return json
            return jsonify({"status": "succes", "my_shop": data})
        except Exception as e:
            return jsonify({"error": str(e)})
        
    elif request.method == 'POST':
        try:
            nama = request.json['nama']
            deskripsi = request.json['deskripsi']
            harga = request.json['harga']
            gambar = request.json['gambar']
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO my_shop(nama, deskripsi, harga, gambar) values(%s, %s, %s, %s)", (nama, deskripsi, harga, gambar),)
            mysql.connection.commit()
            cur.close()
            
            return jsonify({'message': 'data berhasil ditambahkan'})
        except Exception as e:
            return jsonify({"error": str(e)})
    
    # Edit
@app.route('/shop/edit-bloc', methods=['PUT'])
def edit_bloc():
    try:
        data = request.get_json()
        id = data['id']
        nama = data['nama']
        deskripsi = data['deskripsi']
        harga = data['harga']
        gambar = data['gambar']
            
        cur = mysql.connection.cursor()
        cur.execute("UPDATE my_shop SET nama = %s, deskripsi = %s, harga = %s, gambar = %s WHERE id = %s", (nama, deskripsi, harga, gambar, id),)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'data berhasil diubah'})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    # Delete    
@app.route('/shop/<int:id>', methods=['DELETE'])
def delete_shop(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM my_shop WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"message": "data berhasil dihapus"})
    except Exception as e:
        return jsonify({"error": str(e)})   

if __name__ == '__main__':
    app.run(debug=True) 