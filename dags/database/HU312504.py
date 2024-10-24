from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from .connection import get_db
from .models import EmployeeEvaluated, Evaluation, Prompt, Fortaleza, Brecha, Supraconducta


def get_id_sintesis_evaluacion():
  db = next(get_db())
  try:
    query = text(
      """
      SELECT 
        Id,
        IdEmpleadosCHTDQ
      FROM 
        Sintesis_Evaluacion_IA 
      WHERE 
        Estado IN ('Sin Enviar', 'Reprocesar');
      """
    )
    result = db.execute(query)
    id_sintesis_list = result.mappings().fetchall()
    id_sintesis = [sintesis['Id'] for sintesis in id_sintesis_list]
    id_empleados = [sintesis['IdEmpleadosCHTDQ'] for sintesis in id_sintesis_list]

    return id_sintesis, id_empleados 
  except Exception as e:
    print(f"Error GetIdSintesisEvaluacion: {e}")
    return None, None

  


def get_employee_information(employee_id):
  db = next(get_db())
  try:
    query = text(
      """
      SELECT 
        Id AS id,
        IdEmpleado AS id_empleado,
        IdProceso AS id_proceso,
        Poblacion AS poblacion,
        NombreEmpleado AS nombre_empleado,
        ApellidosEmpleados AS apellidos_empleado,
        FechaLimite AS fecha_limite,
        FechaActualizacionProceso AS fecha_actualizacion_proceso,
        CargoEvaluacion AS cargo_evaluacion,
        AreaEvaluacion AS area_evaluacion
      FROM 
        Empleados_Evaluados_CDHTQ 
      WHERE 
        Id = :employee_id;
      """
    )
    result = db.execute(query, {'employee_id': employee_id})
    data_employees = result.mappings().first()
    if data_employees:
      employee = EmployeeEvaluated(**data_employees)
      return employee
    
    return None
      
  except Exception as e:
    print(f"Error GetEmployeeInformation: {e}")
    return None


def get_employee_evaluations(employee_id):
  db = next(get_db())
  try:
    query = text(
      """
      SELECT 
        Id AS id,
        IdEmpleadosCHTDQ AS id_empleado,
        Competencia AS competencia,
        Enunciado AS enunciado,
        Relacion AS relacion,
        Explicacion AS explicacion,
        Comentarios AS comentarios,
        CantidadEvaluadores AS cantidad_evaluadores,
        FrecuenciaRespuesta AS frecuencia_respuesta,
        EstadoEvaluacionRelacion AS estado_relacion,
        EstadoEvaluacionProceso AS estado_proceso
      FROM 
        Evaluaciones_CDHTQ 
      WHERE 
        IdEmpleadosCHTDQ = :employee_id;
      """
    )
    result = db.execute(query, {'employee_id': employee_id})
    data_evaluations = result.mappings().fetchall()
    if data_evaluations:
      evaluations = [Evaluation(**data) for data in data_evaluations]
      return evaluations
    
    return None
  except Exception as e:
    print(f"Error GetEmployeeEvaluations: {e}")
    return None


def get_data_prompts():
  db = next(get_db())
  try:
    query = text(
      """
      SELECT
        p.Id AS id_prompt,
        p.Descripcion AS descripcion,
        p.Plantilla AS plantilla,
        --p.IdTipoLista1,
        --p.IdListaValores1,
        --p.IdTipoLista2,
        --p.IdListaValores2,
        lv1.Descripcion AS poblacion,
        lv2.Descripcion AS nivel_ejecucion
      FROM 
        PROMPTS p
      JOIN 
        LISTA_VALORES lv1
        ON lv1.Id = p.IdListaValores1
        AND lv1.IdTipoLista = p.IdTipoLista1
      JOIN 
        LISTA_VALORES lv2
        ON lv2.Id = p.IdListaValores2
        AND lv2.IdTipoLista = p.IdTipoLista2
      """
    )
    result = db.execute(query)
    data_prompts = result.mappings().fetchall()
    if data_prompts:
      prompts = [Prompt(**data) for data in data_prompts]
      return prompts
    
    return None
  except Exception as e:
    print(f"Error GetDataPrompts: {e}")
    return None


def get_strengths():
  db = next(get_db())
  try:
    query = text(
      """
      SELECT
        Id AS id,
        Fortaleza AS fortaleza,
        Descripcion AS descripcion,
        EstadoActivo AS estado_activo
      FROM
        Fortalezas
      """
    )
    result = db.execute(query)
    data_strengths = result.mappings().fetchall()
    if data_strengths:
      strengths = [Fortaleza(**data) for data in data_strengths]
      return strengths
    
    return None
  except Exception as e:
    print(f"Error GetStrengths: {e}")
    return None

def get_gaps():
  db = next(get_db())
  try:
    query = text(
      """
      SELECT
        Id AS id,
        Brecha AS brecha,
        Descripcion AS descripcion,
        EstadoActivo AS estado_activo
      FROM
        Brechas
      """
    )
    result = db.execute(query)
    data_gaps = result.mappings().fetchall()
    if data_gaps:
      gaps = [Brecha(**data) for data in data_gaps]
      return gaps
    
    return None
  except Exception as e:
    print(f"Error GetGaps: {e}")
    return None
  
def get_supraconductas():
  db = next(get_db())
  try:
    query = text(
      """
      SELECT
        Id AS id,
        Supraconducta AS supraconducta,
        Descripcion AS descripcion,
        EstadoActivo AS estado_activo
      FROM
        SUPRACONDUCTAS
      """
    )
    result = db.execute(query)
    data_behaviors = result.mappings().fetchall()
    if data_behaviors:
      behaviors = [Supraconducta(**data) for data in data_behaviors]
      return behaviors
    
    return None
  except Exception as e:
    print(f"Error GetBehaviors: {e}")