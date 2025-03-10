import './App.css'
import Inventario from './inventario'
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Ventas from './ventas';

function App() {

  return (
    <>
      <Router>

        <Routes>
          <Route path="/" element={<Inventario />} />
          <Route path="/ventas" element={<Ventas />} />
          <Route path="/inventario" element={<Inventario />} />
        </Routes>
      </Router>
    </>
  )
}

export default App
