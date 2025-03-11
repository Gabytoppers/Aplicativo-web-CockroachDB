import {Link} from "react-router-dom";

const Data = [
    [1, "Laptop", 1200.50, 10],
    [2, "Mouse", 25.99, 50],
    [3, "Teclado", 45.00, 30],
    [4, "Monitor", 1500.00, 20],
    [5, "Cargador", 75.00, 40]
];
const Inventario = () => {
    const deleteItem = (message) => {
        alert(message);
        console.log(message);
    }

    const editarItem = (message) => {
        alert(message);
        console.log(message);
    }


    return (
        <div className="container">
            <nav className="navbar">
                <h1 className="logo">Tienda</h1>
                <div className="nav-links">
                    <Link to="/inventario" className="nav-item">Inventario</Link>
                    <Link to="/ventas" className="nav-item">Ventas</Link>
                </div>
            </nav>
            <div className="container-1">
            <h1 className="title">Gestión de Productos</h1>

            <div className="input-group">
                <input className="input" placeholder="Nombre del producto" />
                <input className="input" placeholder="Precio" type="number" />
                <input className="input" placeholder="Stock" type="number" />
            </div>

            <button className="button">
                ➕ Agregar Producto
            </button>

            <div className="grid-container">
                {Data.map(([id, nombre, precio, stock]) => (
                    <div className="card" key={id}>
                        <h2>{nombre}</h2>
                        <p>Precio: ${precio}</p>
                        <p>Stock: {stock}</p>
                        <div className="button-group">
                            <button className="edit-btn" onClick={()=>editarItem(id)}>✏️ Editar</button>
                            <button className="delete-btn" onClick={()=>deleteItem(id)}>🗑 Eliminar</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
        
        </div>


    );
}

export default Inventario;