<template>
  <div class="inventario-container">
    <h1>Gestión de Inventario</h1>
    
    <div v-if="loading" class="loading">Cargando productos...</div>
    <div v-else-if="error" class="error">Error: {{ error.message }}</div>
    
    <div v-else>
      <div class="productos-list">
        <div v-for="producto in productos" :key="producto.id" class="producto-card">
          <div class="producto-header">
            <h3>{{ producto.nombre }}</h3>
            <span class="precio">${{ producto.precio.toFixed(2) }}</span>
          </div>
          
          <div class="producto-body">
            <img :src="producto.imagen || 'https://via.placeholder.com/100'" alt="Imagen producto" class="producto-imagen">
            
            <div class="stock-control">
              <button 
                @click="modificarStock(producto.id, -1)" 
                :disabled="producto.stock <= 0"
                class="stock-btn"
              >
                -
              </button>
              
              <span class="stock-value" :class="{ 'stock-low': producto.stock <= 3 }">
                {{ producto.stock }} {{ producto.stock === 1 ? 'unidad' : 'unidades' }}
              </span>
              
              <button 
                @click="modificarStock(producto.id, 1)" 
                class="stock-btn"
              >
                +
              </button>
            </div>
            
            <div class="disponibilidad" :class="{ 'disponible': producto.disponible, 'no-disponible': !producto.disponible }">
              {{ producto.disponible ? 'Disponible' : 'Agotado' }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useMutation, useQuery } from '@vue/apollo-composable'
import gql from 'graphql-tag'
import { ref } from 'vue'

const PRODUCTOS_QUERY = gql`
  query GetProductos {
    productos {
      id
      nombre
      precio
      stock
      disponible
      imagen
    }
  }
`

export default {
  name: 'InventarioTienda',
  
  setup() {
    const productos = ref([])
    const loading = ref(true)
    const error = ref(null)

    // Eliminamos la variable 'result' que no se usaba
    const { onResult } = useQuery(PRODUCTOS_QUERY, null, {
      fetchPolicy: 'cache-and-network'
    })

    onResult((queryResult) => {
      loading.value = queryResult.loading
      error.value = queryResult.error
      
      if (queryResult.data) {
        productos.value = queryResult.data.productos || []
        console.log('Productos actualizados:', productos.value)
      }
    })

    const { mutate: modificarStockMutation } = useMutation(gql`
      mutation ModificarStock($id: Int!, $cantidad: Int!) {
        modificarStock(id: $id, cantidad: $cantidad) {
          ok
          producto {
            id
            nombre
            precio
            stock
            disponible
            imagen
          }
        }
      }

      
    `, {
      update(cache, { data: { modificarStock } }) {
        try {
          if (modificarStock?.ok) {
            const data = cache.readQuery({ query: PRODUCTOS_QUERY })
            
            if (data?.productos) {
              const updatedProductos = data.productos.map(p => 
                p.id === modificarStock.producto.id ? modificarStock.producto : p
              )
              
              cache.writeQuery({ 
                query: PRODUCTOS_QUERY, 
                data: { productos: updatedProductos }
              })
            }
          }
        } catch (e) {
          console.error('Error actualizando cache:', e)
        }
      }
    })

    const modificarStock = async (id, cantidad) => {
      try {
        console.log(`Modificando stock: ID ${id}, Cantidad ${cantidad}`)
        await modificarStockMutation({ id, cantidad })
      } catch (err) {
        console.error('Error al modificar stock:', err)
        error.value = err
      }
    }

    return {
      productos,
      loading,
      error,
      modificarStock
    }
  }
}
</script>

<style scoped>
.inventario-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
}

.loading, .error {
  padding: 20px;
  text-align: center;
  font-size: 1.2rem;
}

.error {
  color: #e74c3c;
}

.productos-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.producto-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.producto-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
}

.precio {
  font-weight: bold;
  color: #27ae60;
}

.producto-body {
  padding: 15px;
  text-align: center;
}

.producto-imagen {
  max-width: 100%;
  height: 150px;
  object-fit: contain;
  margin-bottom: 15px;
}

.stock-control {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 15px 0;
}

.stock-btn {
  width: 30px;
  height: 30px;
  border: none;
  background-color: #3498db;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.stock-btn:hover {
  background-color: #2980b9;
}

.stock-btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.stock-value {
  margin: 0 15px;
  font-size: 1.1rem;
}

.stock-low {
  color: #e74c3c;
  font-weight: bold;
}

.disponibilidad {
  padding: 5px 10px;
  border-radius: 4px;
  display: inline-block;
  font-weight: bold;
}

.disponible {
  background-color: #2ecc71;
  color: white;
}

.no-disponible {
  background-color: #e74c3c;
  color: white;
}
</style>