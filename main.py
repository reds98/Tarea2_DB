from flask import Flask, render_template, request, url_for, flash, redirect
app = Flask(_name_)
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
        print("RESULT",results[0])
        print(results[0].get('userName'))
        if(results[0].get('UserName')!=None):
            request.method=='GET'
            return articles()
            
        else:
            return render_template('index.html',error='Combinación de usuario/password no existe en la BD')
            # return articles("")


@app.route('/articles',methods=["POST","GET"])
def articles():
    # print("re")
    # print("USER ",user)
    print("request",request.method)
    print("REQUEST FORM",request.form)
    print("ARGS==>",request.args)
    # print("VALOR DEL NOMBRE TU PUEDES", "nombre" in request.form)
    if request.method=="POST" and request.form.get('userName')!=None:
        #  articulos=obtenerArticulos()
        #  print(articulos)
        print("IF")
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        cursor.execute(f"EXEC BuscarArticulosPorNombre @nombreBuscado = '', @user='{1}',@ip='{request.remote_addr}'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.close()
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        categories=[]
        cursor.execute(f"EXEC obtenerClases @user='2',@ip='{request.remote_addr}'")
        for row in cursor:
            categories.append(row)
            print("categorias",row)
        conn.close()
        print("RESULTS",categories)
        return render_template('articles.html',info=results,opciones=categories)
    
    elif(request.args.get('name')!=None):
        print("ELSE de NOMBRE")
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        cursor.execute(f"EXEC BuscarArticulosPorNombre @nombreBuscado = '{request.args['name']}', @user='1',@ip='{request.remote_addr}'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.close()
        print("RESULTS",results)
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        categories=[]
        cursor.execute(f"EXEC obtenerClases @user='2',@ip='{request.remote_addr}'")
        for row in cursor:
            categories.append(row)
            print("categorias",row)
        conn.close()
        print("RESULTS",categories)
        return render_template('articles.html',info=results,opciones=categories)
    elif(request.args.get('amount')!=None):
        print("ELSE de CANTIDAD")
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        cursor.execute(f"EXEC SeleccionarArticulosPorOrdenAlfabetico @n = '{request.args['amount']}', @user='2',@ip='{request.remote_addr}'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.close()
        print("RESULTS",results)
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        categories=[]
        cursor.execute(f"EXEC obtenerClases @user='2',@ip='{request.remote_addr}'")
        for row in cursor:
            categories.append(row)
            print("categorias",row)
        conn.close()
        print("RESULTS",categories)
        return render_template('articles.html',info=results,opciones=categories)
    
    elif(request.args.get('categoria')!=None):
        print("el nombre de la clase es ==>",request.args.get('categoria'))
        print("ELSE de CATEGORIAS")
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        cursor.execute(f"EXEC SeleccionarArticulosPorClase @nombreClase = '{request.args.get('categoria')}', @user='2',@ip='{request.remote_addr}'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.close()
        print("RESULTS",results)
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        categories=[]
        cursor.execute(f"EXEC obtenerClases @user='2',@ip='{request.remote_addr}'")
        for row in cursor:
            categories.append(row)
            print("categorias",row)
        conn.close()
        print("RESULTS",categories)
        return render_template('articles.html',info=results,opciones=categories)
    elif(request.args.get('inputName')!=None):
       
        print("ELSE de INSERTAR")
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        print("valores a insertar==>",request.args.get('inputName'),request.args.get('categoriasInput'),request.args.get('inputPrice'))
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        cursor.execute(f"EXEC InsertarArticulo @nombreArticulo='{request.args.get('inputName')}',@nombreClase='{request.args.get('categoriasInput')}',@precio='{request.args.get('inputPrice')}', @user='2',@ip='{request.remote_addr}'")
        print("DESPUES DE INSERTAR")
        for row in cursor:
            
            print("resultado insertar",row)
        conn.close()
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        cursor.execute(f"EXEC BuscarArticulosPorNombre @nombreBuscado = '', @user='{1}',@ip='{request.remote_addr}'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.close()
        print("RESULTS",results)
        conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        categories=[]
        cursor.execute(f"EXEC obtenerClases @user='2',@ip='{request.remote_addr}'")
        for row in cursor:
            categories.append(row)
            print("categorias",row)
        conn.close()
        print("RESULTS",categories)
      
        return render_template('articles.html',info=results,opciones=categories)
    else:
        print("ESLSE ERROR")
    #     print("ES EL POST")
    #     print("REQUEST FORM",request.form) 
    #     userName=request.form["userName"]
    #     password=request.form["password"]
    #     conn = pymssql.connect('servertarels.database.windows.net', "bd", "Tantan20", "Tarea2")
    #     cursor = conn.cursor(as_dict=True)
    #     print("CONN",conn)
    #     cursor = conn.cursor(as_dict=True)
    #     results=[]
    #     cursor.execute(f"EXEC VerificarCredenciales @nombreUsuario = '{userName}', @password = '{password}'")
    #     for row in cursor:
    #         results.append(row)
    #         print("ROW",row)
    #     conn.close()
    #     if(results[0]['Resultado']=='Credenciales inválidas'):
    #         return render_template('index.html',error='Combinación de usuario/password no existe en la BD')
    #     else:
    #         return render_template('index.html',error='Login correcto')

        
        



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