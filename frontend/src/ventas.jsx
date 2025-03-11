import './ventas.css'
import { Link } from "react-router-dom";
const Ventas = () => {
    const listarPoductos = (message) => {
        alert(message);
        console.log(message);
    };
    
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
                <h1 className="title">Nueva Venta</h1>

                <div className="sales-section">

                    <div className="add-product">
                        <h2>Agregar Productos</h2>
                        <select className="select-product"onClick={()=> listarPoductos()}>
                            <option>Producto 1 - $100</option>
                            <option>Producto 2 - $200</option>
                        </select>
                        <input type="number" className="input" placeholder="Cantidad" />
                        <button className="button add-btn" >🛒 Agregar a la venta</button>
                    </div>

                    <div className="sales-summary">
                        <h2>Resumen de Venta</h2>
                        <div className="summary-item">
                            <p>Producto 1 <br /> <span>3 x $100</span></p>
                            <p>$300</p>
                        </div>
                        <div className="summary-item">
                            <p>Producto 2 <br /> <span>10 x $200</span></p>
                            <p>$2000</p>
                        </div>
                        <hr />
                        <div className="total">
                            <p><strong>Total:</strong></p>
                            <p><strong>$2300</strong></p>
                        </div>
                        <button className="button download-btn">📂 Finalizar y Descargar CSV</button>
                    </div>
                </div>
            </div>

        </div>

    )
}

export default Ventas;