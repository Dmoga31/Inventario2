# [Instalación y configuración de proyecto](https://github.com/Dmoga31/Inventario2/blob/main/Instalacion_Config.md)

# Preguntas
## ¿Qué ventajas ofrece GraphQL sobre REST en este contexto?
- **Precisión en las consultas**: El frontend puede solicitar exactamente los campos que necesita (como `stock` y `disponible`), evitando sobre-fetching.
  ```python
  class Producto(graphene.ObjectType):
      id = graphene.Int()
      nombre = graphene.String()
      precio = graphene.Float()
      stock = graphene.Int()
      disponible = graphene.Boolean()
      imagen = graphene.String()
  ```

- **Múltiples operaciones en una solicitud**: Consultas y mutaciones (como actualizar stock y recibir el nuevo estado) se completan en un solo request.
  ```python
  class Query(graphene.ObjectType):
      productos = graphene.List(Producto)
  
  class Mutation(graphene.ObjectType):
      modificar_stock = ModificarStock.Field()
  ```
  
- **Tipado fuerte**: El esquema GraphQL sirve como documentación autoexplicativa y previene errores.
  ```python
  class ModificarStock(graphene.Mutation):
      class Arguments:
          id = graphene.Int(required=True)
          cantidad = graphene.Int(required=True) 
  ```

  
- **Flexibilidad**: Fácil evolucionar la API sin versionado (ej: añadir campo `imagen` sin romper clientes existentes).
    ```python
    # Versión inicial
    class Producto(graphene.ObjectType):
        id = graphene.Int()
        nombre = graphene.String()
    
    # Actualización sin romper cambios
    class Producto(graphene.ObjectType):
        imagen = graphene.String()  # Nuevo campo añadido
    ```
## ¿Cómo se definen los tipos y resolvers en una API con GraphQL?

- **Definición de tipos**: Cada campo tiene un tipo específico (`Int`, `String`, `Boolean`, etc.)
  ```python
  class Producto(graphene.ObjectType):
      id = graphene.Int()
      nombre = graphene.String()
      precio = graphene.Float()
      stock = graphene.Int()
      disponible = graphene.Boolean()
      imagen = graphene.String()
  ```

- **Resolvers**: Los "Resolver de consulta" o "Querys" son funcioens que **obtienen** datos (operaciones ´`GET` equivalentes en REST) y los "Resolvers de mutación" son funcioes que **modifican** datos (operaciones `POST/PUT/DELETE` equivalentes en REST)

  ### Querys
  ```python
  class Query(graphene.ObjectType):
      productos = graphene.List(Producto)  # Define qué devuelve
      
      def resolve_productos(self, info):
          # Lógica para obtener productos
          return productos  # Devuelve los datos concretos
  ```

  ### Resolvers de mutación
  ```python
  class ModificarStock(graphene.Mutation):
      class Arguments:
          id = graphene.Int(required=True)
          cantidad = graphene.Int(required=True)
      
      ok = graphene.Boolean()
      producto = graphene.Field(Producto)
      
      def mutate(self, info, id, cantidad):
          # 1. Lógica de negocio
          producto = next((p for p in productos if p["id"] == id)
          producto["stock"] += cantidad
          
          # 2. Actualización de estado
          producto["disponible"] = producto["stock"] > 0
          
          # 3. Retorna el tipo definido
          return ModificarStock(
              ok=True,
              producto=producto  # Conversión automática a tipo Producto
          )
  ```
## ¿Por qué es importante que el backend también actualice disponible y no depender solo del frontend?
 - **Consistencia**: Diferentes clientes podrían mostrar estados diferentes.
   - Ejemplo: La app móvil muestra "disponible" mientras la web mestra "agotado"
    ### Ejemplo en código
    ```python
    producto["stock"] += cantidad
    producto["disponible"] = producto["stock"] > 0 
    ```
  - **Seguridad**: Si alguien intenta enviar `disponible: true` con stock **0**
      ```python
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
      ```

  - **Única fuente verdadera**: Una única regla de negocio centralizada:
      ```python
       producto["disponible"] = producto["stock"] > 0
      ```
      Los cambios se aplican globalmente (ej: modificar a `stock > 5` solo requiere          cambiar el backend)


## ¿Cómo garantizas que la lógica de actualización de stock y disponibilidad sea coherente?

## Garantía de Coherencia: Stock vs Disponible

| Escenario               | Problema Potencial           | Solución Implementada          |
|-------------------------|------------------------------|--------------------------------|
| **Stock negativo**      | Disponible mostraría `True` aunque el stock sea inválido | `stock = max(0, stock)` (Fuerza stock mínimo a 0) |
| **Frontend manipulado** | Cliente podría enviar `disponible: True` con stock `0` | Lógica 100% en backend (`disponible = stock > 0`) |
| **Múltiples clientes**  | Apps móvil/web mostrarían estados distintos | Única fuente de verdad en el backend |
| **Caché obsoleta**     | Frontend mostraría datos desactualizados | Mutaciones siempre devuelven el estado actualizado |
| **Cambios futuros**     | Requeriría actualizar todos los clientes | Reglas de negocio centralizadas (ej: modificar a `stock > 5` solo en backend) |

**Código**:  
```python
producto["stock"] = max(0, producto["stock"] + cantidad)  # 1. Valida stock
producto["disponible"] = producto["stock"] > 0           # 2. Actualiza
```
