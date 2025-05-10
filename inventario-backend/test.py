import pytest
from app import app, productos

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_stock_cero_actualiza_disponible():
    """Verifica que al llegar a stock 0, disponible sea False"""
    test_product = {
        "id": 99,
        "nombre": "Producto Test",
        "precio": 1.99, 
        "stock": 1,
        "disponible": True,
        "imagen": ""  
    }
    productos.append(test_product)
    
    query = """
    mutation {
        modificarStock(id: 99, cantidad: -1) {
            producto {
                stock
                disponible
            }
        }
    }
    """
    with app.test_client() as client:
        response = client.post('/graphql', json={'query': query})
        assert response.status_code == 200
        data = response.get_json()
        assert data['data']['modificarStock']['producto']['stock'] == 0
        assert data['data']['modificarStock']['producto']['disponible'] is False

def test_stock_positivo_desde_cero():
    """Verifica que al aumentar stock desde 0, disponible sea True"""
    test_product = {
        "id": 100,
        "nombre": "Producto Test 2",
        "precio": 2.99,  
        "stock": 0,
        "disponible": False,
        "imagen": ""
    }
    productos.append(test_product)
    
    query = """
    mutation {
        modificarStock(id: 100, cantidad: 3) {
            producto {
                stock
                disponible
            }
        }
    }
    """
    with app.test_client() as client:
        response = client.post('/graphql', json={'query': query})
        assert response.status_code == 200
        data = response.get_json()
        assert data['data']['modificarStock']['producto']['stock'] == 3
        assert data['data']['modificarStock']['producto']['disponible'] is True

