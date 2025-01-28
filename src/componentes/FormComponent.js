import React, { useState } from 'react';
 
const FormComponent = () => {
    const [name, setName] = useState('');
    const [response, setResponse] = useState('');
 
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await api.get('/usuarios', { name });
            setResponse(res.data.message); // Asumiendo que la respuesta tiene un campo "message"
        } catch (error) {
            console.error("Error al llamar a la API:", error);
        }
    };

    return (
<form onSubmit={handleSubmit}>
<label>
                Nombre:
<input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
</label>
<button type="submit">Enviar</button>
            {response && <p>Respuesta de la API: {response}</p>}
</form>
    );
};
 
export default FormComponent;