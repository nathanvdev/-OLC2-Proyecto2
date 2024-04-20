import '../styles/App.css'
import '../styles/NavBar.css'
import '../styles/Images.css'

import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.min.css';





function Reports() {
    const [symbols, setSymbols] = useState([]);
    const [errors, setErrors] = useState([]);
    const apiUrl = "http://127.0.0.1:5000"


    const GetReports = async () => {
        try {
            const response = await axios.post(apiUrl + '/reports/all');
            console.log('Respuesta del servidor:', response);
    
            if (response.data) {
                const { symbols, errors } = response.data;
                console.log('Symbols:', symbols);
                console.log('Errors:', errors);
    
                // Aquí puedes procesar symbols y errors como necesites.
                // Por ejemplo, podrías establecer el estado de tu componente con estos datos:
                setSymbols(symbols);
                setErrors(errors);
            }
        } catch (error) {
            console.error('Error al enviar la URL al servidor:', error);
        }
    }


    const navigate = useNavigate();


    const returnHome = () => {
        navigate('/');
    };


    return (

        <>
            <div className="item-0">
                <div className="container-NavB">

                    <div className="item-1-NavB">
                        <button className="button-74" role="button" onClick={returnHome}>Home</button>
                    </div>

                    <div className="item-6-NavB">
                        <button className="button-74" role="button" onClick={GetReports}>Reportes</button>
                    </div>

                </div>
            </div>



            <br />
            <br />
            <h1>Tabla de errores</h1>

            <table className="table">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Descripcion</th>
                        <th scope="col">Ambito</th>
                        <th scope="col">Linea</th>
                        <th scope="col">Columna</th>
                        <th scope="col">Tipo</th>
                    </tr>
                </thead>
                <tbody>
                    {errors.map((error, index) => (
                        <tr key={index}>
                            <th scope="row">{index + 1}</th>
                            <td>{error.Descricion}</td>
                            <td>{error.Ambito}</td>
                            <td>{error.Linea}</td>
                            <td>{error.Columna}</td>
                            <td>{error.Tipo}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <br />
            <br />
            <h1>Tabla de simbolos</h1>

            <table className="table">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">ID</th>
                        <th scope="col">Tipo Simbolo</th>
                        <th scope="col">Ambito</th>
                        <th scope="col">Linea</th>
                        <th scope="col">Columna</th>
                    </tr>
                </thead>
                <tbody>
                    {symbols.map((symbol, index) => (
                        <tr key={index}>
                            <th scope="row">{index + 1}</th>
                            <td>{symbol.id}</td>
                            <td>{symbol.symbol_type}</td>
                            <td>{symbol.ambito}</td>
                            <td>{symbol.line}</td>
                            <td>{symbol.column}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

        </>
    )
}

export default Reports;
