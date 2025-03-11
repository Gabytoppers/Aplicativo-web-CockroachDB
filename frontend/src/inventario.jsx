import {Link} from "react-router-dom";
const Inventario = () => {
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
                <div className="card">
                    <h2>Gaseosa</h2>
                    <p>Precio: $3000</p>
                    <p>Stock: 50</p>
                    <div className="button-group">
                        <button className="edit-btn">✏️ Editar</button>
                        <button className="delete-btn">🗑 Eliminar</button>
                    </div>
                </div>

                <div className="card">
                    <h2>Arroz</h2>
                    <p>Precio: $6000</p>
                    <p>Stock: 40</p>
                    <div className="button-group">
                        <button className="edit-btn">✏️ Editar</button>
                        <button className="delete-btn">🗑 Eliminar</button>
                    </div>
                </div>

                <div className="card">
                    <h2>Cerveza</h2>
                    <p>Precio: $10000</p>
                    <p>Stock: 60</p>
                    <div className="button-group">
                        <button className="edit-btn">✏️ Editar</button>
                        <button className="delete-btn">🗑 Eliminar</button>
                    </div>
                </div>
            </div>
        </div>
        
        </div>


    );
}

export default Inventario;