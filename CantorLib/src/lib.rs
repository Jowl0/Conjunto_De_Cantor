use pyo3::prelude::*;

#[pyfunction]
fn conjunto_de_cantor(iteraciones: u32) -> PyResult<Vec<(f64, f64)>> {
    let mut intervalos = vec![(0.0, 1.0)];

    for _ in 0..iteraciones {
        let mut nuevos_intervalos = Vec::with_capacity(intervalos.len() * 2);
        
        for (inicio, fin) in intervalos {
            let distancia = (fin - inicio) / 3.0;
            
            nuevos_intervalos.push((inicio, inicio + distancia));
            nuevos_intervalos.push((fin - distancia, fin));
        }
        intervalos = nuevos_intervalos;
    }

    Ok(intervalos)
}

#[pymodule]
fn CantorLib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(conjunto_de_cantor, m)?)?;
    Ok(())
}