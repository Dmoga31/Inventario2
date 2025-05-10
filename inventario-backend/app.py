from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS  
import graphene

app = Flask(__name__)


CORS(app, resources={
    r"/graphql": {
        "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
        "methods": ["OPTIONS", "POST", "GET"],
        "allow_headers": ["Content-Type"]
    }
})

class Producto(graphene.ObjectType):
    id = graphene.Int()
    nombre = graphene.String()
    precio = graphene.Float()
    stock = graphene.Int()
    disponible = graphene.Boolean()
    imagen = graphene.String()

class Query(graphene.ObjectType):
    productos = graphene.List(Producto)
    
    def resolve_productos(self, info):
        return productos

class ModificarStock(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        cantidad = graphene.Int(required=True)
    
    ok = graphene.Boolean()
    producto = graphene.Field(Producto)
    
    def mutate(self, info, id, cantidad):
       
        producto = next((p for p in productos if p["id"] == id), None)
        if not producto:
            return ModificarStock(ok=False, producto=None)
        
        
        producto["stock"] += cantidad
        
       
        if producto["stock"] < 0:
            producto["stock"] = 0
        
      
        producto["disponible"] = producto["stock"] > 0
        
       
        return ModificarStock(
    ok=True,
    producto=Producto(
        id=producto["id"],
        nombre=producto["nombre"],
        precio=producto.get("precio", 0.0),  
        stock=producto["stock"],
        disponible=producto["disponible"],
        imagen=producto.get("imagen", "") 
    )
)
    
class Mutation(graphene.ObjectType):
    modificar_stock = ModificarStock.Field()



productos = [
    {"id": 1, "nombre": "Manzana", "precio": 0.5, "stock": 5, "disponible": True, "imagen": "https://www.frutality.es/wp-content/uploads/manzana-royal.png"},
    {"id": 2, "nombre": "Banana", "precio": 0.3, "stock": 0, "disponible": False, "imagen": "https://i0.wp.com/upload.wikimedia.org/wikipedia/commons/thumb/6/69/Banana.png/300px-Banana.png" }
]



app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=graphene.Schema(query=Query, mutation=Mutation),
        graphiql=True 
    )
)

if __name__ == '__main__':
    app.run(debug=True)