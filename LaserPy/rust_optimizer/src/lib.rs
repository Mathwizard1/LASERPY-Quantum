use pyo3::prelude::*;

mod universal_constants;
use universal_constants::UniversalConstant;

/// Main python module entrypoint for rust_utils
#[pymodule(name= "rust_optimizer")]
fn rust_optimizer(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<UniversalConstant>()?;
    Ok(())
}
