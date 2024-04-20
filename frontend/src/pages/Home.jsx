import '../styles/App.css'
import '../styles/NavBar.css'
import '../styles/Consoles.css'

import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';





function Home() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [commands_list, setCommands_list] = useState([]);
  const [isPaused, setIsPaused] = useState(false);
  const textAreaRef = useRef(null);
  const apiUrl = "http://127.0.0.1:5000"




  const OpenFile = () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target.result;
        setInput("")
        setInput(content);
      };
      reader.readAsText(file);
    });
    fileInput.click();
    setOutput('');
  };


  const handleSubmit = () => {
    //Para enfocar el textarea
    textAreaRef.current.focus();
    //Para limpiar el textarea
    setOutput('');
    //Para dividir los comandos por salto de línea
    const commandLines = input
    //Actualizamos la lista de comandos y enviamos los comandos
    setCommands_list(commandLines);
    sendCommands(commandLines);
  };

  const sendCommands = async (commands) => {
    if (!commands) {
      console.error('No se proporcionaron comandos para enviar.');
      return;
    }

    try {
      const response = await fetch(`${apiUrl}/send_command`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code_in: commands }),
      });

      if (!response.ok) {
        throw new Error(`Error en la solicitud: ${response.statusText}`);
      }

      const data = await response.json();
      if (data.response != '') {
        setOutput(data.response);
        console.log(data.symbols);
      }


      console.log(errors)
    } catch (error) {
      console.error(`Error en la solicitud: ${error.message}`);
    }
  };


  useEffect(() => {
    if (textAreaRef.current) {
      textAreaRef.current.scrollTop = textAreaRef.current.scrollHeight;
    }
  }, [output]);


  const navigate = useNavigate();

  const handleButtonClick = () => {
    console.log('The link was clicked.');
    navigate('/reports');
  };

  return (
    <>
      <div className="item-0">
        <div className="container-NavB">

          <div className="item-1-NavB">
            <button className="button-74" role="button" onClick={OpenFile}>Abrir Archivo</button>
          </div>

          <div className="item-7-NavB">
            <button className="button-74" role="button" onClick={handleSubmit}>Traducir</button>
          </div>

          <div className="item-1-NavB">
            <button className="button-74" role="button" onClick={OpenFile}>Home</button>
          </div>

          <div className="item-6-NavB">
            <button className="button-74" role="button" onClick={handleButtonClick}>Reportes</button>
          </div>

        </div>
      </div>


      <br />
      <br />

      <div className="item-2">

        <textarea
          type="text"
          className="input-74"
          id='console_input'
          placeholder="input commands"
          value={input}
          onChange={(e) => setInput(e.target.value)}>
        </textarea>

        <textarea
          readOnly
          className="input-75"
          placeholder="output"
          value={output}
          ref={textAreaRef}>
        </textarea>

      </div>

    </>
  )
}

export default Home;
