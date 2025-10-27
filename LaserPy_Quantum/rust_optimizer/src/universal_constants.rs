use pyo3::prelude::*;
use pyo3::pyclass::CompareOp;

/// Enum for universal physical constants
#[pyclass]
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum UniversalConstant {
    SpeedOfLight,
    PlanckConstant,
    ElementaryCharge,
    BoltzmannConstant,
    AvogadroConstant,
}

#[pymethods]
impl UniversalConstant {
    /// Return the value of the constant as f64
    pub fn value(&self) -> f64 {
        match self {
            UniversalConstant::SpeedOfLight => 2.99792458e8,           // m/s
            UniversalConstant::PlanckConstant => 6.62607015e-34,       // J·s
            UniversalConstant::ElementaryCharge => 1.602176634e-19,    // C
            UniversalConstant::BoltzmannConstant => 1.380649e-23,      // J/K
            UniversalConstant::AvogadroConstant => 6.02214076e23,      // 1/mol
        }
    }

    /// human-readable name
    pub fn name(&self) -> &'static str {
        match self {
            UniversalConstant::SpeedOfLight => "SpeedOfLight",
            UniversalConstant::PlanckConstant => "PlanckConstant",
            UniversalConstant::ElementaryCharge => "ElementaryCharge",
            UniversalConstant::BoltzmannConstant => "BoltzmannConstant",
            UniversalConstant::AvogadroConstant => "AvogadroConstant",
        }
    }

    /// Show nicely in Python REPL
    fn __repr__(&self) -> String {
        format!("<UniversalConstant.{} = {}>", self.name(), self.value())
    }

    fn __str__(&self) -> String {
        self.__repr__()
    }

    fn __richcmp__(&self, other: PyRef<'_, Self>, op: CompareOp) -> bool {
        match op {
            CompareOp::Eq => self.value() == other.value(),
            CompareOp::Ne => self.value() != other.value(),
            _ => false,
        }
    }
}
