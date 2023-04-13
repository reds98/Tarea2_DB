from flask import Flask, render_template, request, url_for, flash, redirect
app = Flask(__name__)
import pymssql


#     print("ID=%d, Name=%s" % (row['id'], row['name']))
def obtenerArticulos():
    conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
    cursor = conn.cursor(as_dict=True)
    results=[]
    cursor.execute('EXEC dbo.SelectArticles;')
    for row in cursor:
        results.append(row)
        print(row)
    conn.commit()
    conn.close()
    return results
#     print("ID=%d, Name=%s" % (row['id'], row['name']))
def insertarArticulo(nombre,precio):
    
    conn = pymssql.connect("basescurso.database.windows.net", "adminBases", "Tantan20", "dbTarea1")
    cursor = conn.cursor(as_dict=True)
    results=[]
    cursor.execute(f"EXEC InsertArticle @article_name ='{nombre}' , @price ={precio} ;")
    for row in cursor:
        results.append(row)
        print(row)
    conn.commit()
    conn.close()
    return results
@app.route('/',methods=["POST","GET"])
def index():
    if request.method=="GET":
        #  articulos=obtenerArticulos()
        #  print(articulos)
       
        return render_template('index.html',error='')
    else:
        print("ES EL POST")
        print("REQUEST FORM",request.form) 
        userName=request.form["userName"]
        password=request.form["password"]
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        cursor.execute(f"EXEC VerificarCredenciales @nombreUsuario = '{userName}', @password = '{password}'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.close()
        if(results[0]['Resultado']=='Credenciales inválidas'):
            return render_template('index.html',error='Combinación de usuario/password no existe en la BD')
        else:
            return render_template('index.html',error='Login correcto')

        
        



@app.route('/createArticle',methods=["POST","GET"])
def createArticle():
    if request.method=="POST":
        print("ES EL POST")
        print("REQUEST FORM",request.form)
        if (request.form['articlePrice']):
            print("DENTRO DEL IF")
            articleName=request.form["articleName"]
            articlePrice=request.form["articlePrice"]
            print("DATA TO BE INSERTED ",articleName,articlePrice)
            resultInsert=insertarArticulo(articleName,articlePrice)
            result=resultInsert[0]["Result"]
            print("INSERT RESULT==>",resultInsert[0])
            print("KEYS",result)
            if(result=="Article with the name Martillo already exists."):
                return render_template('create.html',error=result)
            else:
                articulos=obtenerArticulos()
                return render_template('index.html',articulos=articulos,message=result) 


        
    #  print(articulos)
        
    else:
        return render_template('create.html')