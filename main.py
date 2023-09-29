from flask import Flask, render_template, request, url_for, flash, redirect
app = Flask(__name__)
import pymssql


#     print("ID=%d, Name=%s" % (row['id'], row['name']))
def obtenerArticulos():
    print("Hola obtener articulos")
    conn = pymssql.connect('planilladocente.database.windows.net', "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
    cursor = conn.cursor(as_dict=True)
    results=[]
    cursor.execute('EXEC BuscarArticulos  @article_name ='';')
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





@app.route('/', methods=["POST", "GET"])
def index():
    error = ''
    
    if request.method == "POST":
        userName = request.form["userName"]
        password = request.form["password"]
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        results = []
        ip = request.remote_addr

        cursor.execute(f"EXEC Login @UserName = '{userName}', @Password = '{password}', @PostIP ='{ip}'")
        
        for row in cursor:
            results.append(row)
        conn.commit()
        conn.close()
        print("RESULTADO ELEMENTO 0",results[0])
        if results and results[0] != {'id': -1, 'UserName': ''}:
            user_id = results[0]['id']
            # return redirect(url_for('articles', user_id=user_id))
            # return redirect(url_for('articles', user_id=user_id))
            return redirect(url_for('articles',userId=user_id))

        else:
            error = 'Combinación de usuario/password no existe en la BD'
    
    return render_template('index.html', error=error)


@app.route('/createArticle', methods=["POST", "GET"])
def createArticle():
    error = ''
    
    if request.method == "POST":
        userName = request.form["userName"]
        password = request.form["password"]
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        results = []
        ip = request.remote_addr

        cursor.execute(f"EXEC Login @UserName = '{userName}', @Password = '{password}', @PostIP ='{ip}'")
        
        for row in cursor:
            results.append(row)
        conn.commit()
        conn.close()
        print("RESULTADO ELEMENTO 0",results[0])
        if results and results[0] != {'id': -1, 'UserName': ''}:
            user_id = results[0]['id']
            # return redirect(url_for('articles', user_id=user_id))
            # return redirect(url_for('articles', user_id=user_id))
            return redirect(url_for('articles',userId=user_id))

        else:
            error = 'Combinación de usuario/password no existe en la BD'
    
    return render_template('create.html', error=error)



@app.route('/searchForDelete', methods=["POST", "GET"])
def searchForDelete():
    error = ''
    user_id = request.args.get('userId')
    codigo = request.args.get('codigo')
    print("USER ID SEARCH ITEM",user_id)
    if request.method == "POST":
        codigo = request.form["Codigo"]
        print("CODIGO A BUSCAR PARA ELIMINAR",codigo)
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        #  EXEC BuscarArticulos @Filtro ='',@UsuarioId='1', @PostIP = '192.168.1.100';
        # EXEC BuscarArticuloPorCodigoParaBorrar @CodigoArticulo = 'AT0s01', @UsuarioId = 3, @PostIP = '192.168.1.100';

        cursor.execute(f"EXEC BuscarArticuloPorCodigoParaBorrar @CodigoArticulo = '{codigo}', @UsuarioId='{user_id}', @PostIP = '192.168.1.100'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.commit()
        conn.close()

        if results and results[0]["Result"]!="No se encontró":
            print("Si se encontro")
            return redirect(url_for('deleteItem',userId=user_id,codigo=codigo))

        else:
            print("No se encontro")
            error = 'No se encontro el articulo a borrar'
    
    return render_template('searchForDelete.html', error=error)



@app.route('/deleteItem', methods=["POST", "GET"])
def deleteItem():
    error = ''
    user_id = request.args.get('userId')
    codigo = request.args.get('codigo')
    print("USER ID DELETE ITEM",user_id)
    print("CODIGO DELETE ITEM",codigo)
    conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
    cursor = conn.cursor(as_dict=True)
    print("CONN",conn)
    cursor = conn.cursor(as_dict=True)
    results=[]
    cursor.execute(f"EXEC BuscarArticuloPorCodigoParaBorrar @CodigoArticulo = '{codigo}', @UsuarioId='{user_id}', @PostIP = '192.168.1.100'")
    for row in cursor:
        results.append(row)
        print("ROW",row)
    conn.commit()
    conn.close()
    articulo=results[0]
    if request.method == "POST":
        print("CODIGO A BUSCAR PARA ELIMINAR",codigo)
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        #  EXEC BuscarArticulos @Filtro ='',@UsuarioId='1', @PostIP = '192.168.1.100';
        # EXEC BuscarArticuloPorCodigoParaBorrar @CodigoArticulo = 'AT0s01', @UsuarioId = 3, @PostIP = '192.168.1.100';
        # EXEC BorrarArticulo @CodigoArticulo = 'AT001', @UsuarioId = 3, @PostIP = '192.168.1.100';

        cursor.execute(f"EXEC BorrarArticulo @CodigoArticulo = '{codigo}', @UsuarioId='{user_id}', @PostIP = '192.168.1.100'")
        for row in cursor:
            results.append(row)
            print("ROW AFTER DELETING",row)
        conn.commit()
        conn.close()

        return redirect(url_for('articles',userId=user_id))
    
    return render_template('deleteItem.html', error=error,articulo=articulo)





@app.route('/articles', methods=["POST", "GET"])
def articles():
    user_id = request.args.get('userId')
    categoria = request.args.get('categoria')
    cantidad = request.args.get('cantidad')
    nombre = request.args.get('nombre')

    # PARA INSERTAR
    inputName = request.args.get('inputName')
    categoriasInput = request.args.get('categoriasInput')
    inputPrice = request.args.get('inputPrice')
    inputCode = request.args.get('inputCode')


    print("USERID",user_id)

    if categoria:
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        #  EXEC BuscarArticulos @Filtro ='',@UsuarioId='1', @PostIP = '192.168.1.100';
        # EXEC FiltrarPorNombreClaseArticulo @NombreClaseArticulo = 'Electricidad'

        cursor.execute(f"EXEC FiltrarPorNombreClaseArticulo @NombreClaseArticulo = '{categoria}', @UsuarioId='{user_id}', @PostIP = '192.168.1.100'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.commit()
        conn.close()
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        categories=[]
        cursor.execute(f"EXEC ObtenerCategorias")
        print("***********************************************")
        for row in cursor:
            categories.append(row)
            print("categorias",row)
        conn.close()
        print("RESULTS",categories)
        return render_template('articles.html',info=results,opciones=categories)

    elif cantidad:
       conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
       cursor = conn.cursor(as_dict=True)
       print("CONN",conn)
       cursor = conn.cursor(as_dict=True)
       results=[]

       #    EXEC FiltrarPorCantidad @Cantidad = 3, @UsuarioId = 2, @PostIP = '192.168.1.100';

       cursor.execute(f"EXEC FiltrarPorCantidad @Cantidad = '{cantidad}', @UsuarioId='{user_id}', @PostIP = '192.168.1.100'")
       for row in cursor:
           results.append(row)
           print("ROW",row)
       conn.commit()
       conn.close()
       conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
       cursor = conn.cursor(as_dict=True)
       print("CONN",conn)
       cursor = conn.cursor(as_dict=True)
       categories=[]
       cursor.execute(f"EXEC ObtenerCategorias")
       print("***********************************************")
       for row in cursor:
           categories.append(row)
           print("categorias",row)
       conn.close()
       print("RESULTS",categories)
       return render_template('articles.html',info=results,opciones=categories)

    elif nombre:
        # Si nombre tiene un valor, hacer algo con él
        # Por ejemplo, buscar artículos por nombre
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        #EXEC BuscarArticulos @Filtro = '', @UsuarioId = 2, @PostIP = '192.168.1.100';
 
        cursor.execute(f"EXEC BuscarArticulos @Filtro = '{nombre}', @UsuarioId='{user_id}', @PostIP = '192.168.1.100'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.commit()
        conn.close()
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        categories=[]
        cursor.execute(f"EXEC ObtenerCategorias")
        print("***********************************************")
        for row in cursor:
            categories.append(row)
            print("categorias",row)
        conn.close()
        print("RESULTS",categories)
        return render_template('articles.html',info=results,opciones=categories)

    # ELIF PARA INSERTAR UN NUEVO ARTICULO


    # EXEC InsertarArticulo 
    # @Nombre,
    # @NombreClase,
    # @Precio,
    # @Codigo,
    # @UsuarioId,
    # @PostIP;

    elif inputName and categoriasInput and inputPrice and inputCode :
        print("VALORES")
        print("INPUT NAME",inputName)
        # Si nombre tiene un valor, hacer algo con él
        # Por ejemplo, buscar artículos por nombre
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        #EXEC BuscarArticulos @Filtro = '', @UsuarioId = 2, @PostIP = '192.168.1.100';
 
        cursor.execute(f"EXEC InsertarArticulo  @Nombre = '{inputName}' , @NombreClase = '{categoriasInput}',@Precio={int(inputPrice)} ,@Codigo={inputCode}, @UsuarioId='{user_id}', @PostIP = '192.168.1.100'")
        for row in cursor:
            results.append(row)
            print("ROW of inserttion",row)
        conn.commit()
        conn.close()

        # obtenemos todos los datos de nuevo
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        #  EXEC BuscarArticulos @Filtro ='',@UsuarioId='1', @PostIP = '192.168.1.100';

        cursor.execute(f"EXEC BuscarArticulos @Filtro = '', @UsuarioId='{user_id}', @PostIP = '192.168.1.100'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.commit()
        conn.close()

        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        categories=[]
        cursor.execute(f"EXEC ObtenerCategorias")
        print("***********************************************")
        for row in cursor:
            categories.append(row)
            print("categorias",row)
        conn.close()
        print("RESULTS",categories)
        return render_template('articles.html',info=results,opciones=categories)


    else:
        # Si no se proporcionaron parámetros opcionales, mostrar algo por defecto
        #  articulos=obtenerArticulos()
        #  print(articulos)
        print("IF")
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        results=[]
        #  EXEC BuscarArticulos @Filtro ='',@UsuarioId='1', @PostIP = '192.168.1.100';

        cursor.execute(f"EXEC BuscarArticulos @Filtro = '', @UsuarioId='{user_id}', @PostIP = '192.168.1.100'")
        for row in cursor:
            results.append(row)
            print("ROW",row)
        conn.commit()
        conn.close()
        conn = pymssql.connect('planilladocente.database.windows.net',  "adm_user", "QTQ4#eDdeIXw+49F", "Test2")
        cursor = conn.cursor(as_dict=True)
        print("CONN",conn)
        cursor = conn.cursor(as_dict=True)
        categories=[]
        cursor.execute(f"EXEC ObtenerCategorias")
        print("***********************************************")
        for row in cursor:
            categories.append(row)
            print("categorias",row)
        conn.close()
        print("RESULTS",categories)
        return render_template('articles.html',info=results,opciones=categories)




        



# @app.route('/createArticle',methods=["POST","GET"])
# def createArticle():
#     if request.method=="POST":
#         print("ES EL POST")
#         print("REQUEST FORM",request.form)
#         if (request.form['articlePrice']):
#             print("DENTRO DEL IF")
#             articleName=request.form["articleName"]
#             articlePrice=request.form["articlePrice"]
#             print("DATA TO BE INSERTED ",articleName,articlePrice)
#             resultInsert=insertarArticulo(articleName,articlePrice)
#             result=resultInsert[0]["Result"]
#             print("INSERT RESULT==>",resultInsert[0])
#             print("KEYS",result)
#             if(result=="Article with the name Martillo already exists."):
#                 return render_template('create.html',error=result)
#             else:
#                 articulos=obtenerArticulos()
#                 return render_template('index.html',articulos=articulos,message=result) 


        
#     #  print(articulos)
        
#     else:
#         return render_template('create.html')