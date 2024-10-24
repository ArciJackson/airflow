class EmployeeEvaluated:
  def __init__(self, id, id_empleado, id_proceso, poblacion, nombre_empleado, apellidos_empleado, fecha_limite, fecha_actualizacion_proceso, cargo_evaluacion, area_evaluacion):

    self.id = id
    self.id_empleado = id_empleado
    self.id_proceso = id_proceso
    self.poblacion = poblacion
    self.nombre_empleado = nombre_empleado
    self.apellidos_empleado = apellidos_empleado
    self.fecha_limite = fecha_limite
    self.fecha_actualizacion_proceso = fecha_actualizacion_proceso
    self.cargo_evaluacion = cargo_evaluacion
    self.area_evaluacion = area_evaluacion
    self.evaluaciones = []
    self.prompts = []
    self.fortalezas = []
    self.brechas = []
    self.supradonductas = []

  def add_evaluation(self, evaluacion):
    self.evaluaciones.append(evaluacion)

  def add_prompt(self, prompt):
    self.prompts.append(prompt)

  def get_prompts_description(self):
    return [prompt.get_description() for prompt in self.prompts]

  def add_strengths(self, fortalezas):
    if all(isinstance(fortaleza, Fortaleza) for fortaleza in fortalezas):
      self.fortalezas.extend(fortalezas)

  def get_strengths(self):
    return [fortaleza.mostrar_info() for fortaleza in self.fortalezas]

  def add_gaps(self, brechas):
    if all(isinstance(brecha, Brecha) for brecha in brechas):
      self.brechas.extend(brechas)

  def get_gaps(self):
    return [brecha.mostrar_info() for brecha in self.brechas]
  
  def add_supraconductas(self, supradonductas):
    if all(isinstance(supraconducta, Supraconducta) for supraconducta in supradonductas):
      self.supradonductas.extend(supradonductas)

  def __str__(self):
    return f"{self.nombre_empleado} {self.apellidos_empleado} ({self.id_empleado} - {self.poblacion})"



class Evaluation:
  def __init__(self, id, id_empleado, competencia, enunciado, relacion, explicacion, comentarios, cantidad_evaluadores, frecuencia_respuesta, estado_relacion, estado_proceso):
    self.id = id
    self.id_empleado = id_empleado
    self.competencia = competencia
    self.enunciado = enunciado
    self.relacion = relacion
    self.explicacion = explicacion
    self.comentarios = comentarios
    self.cantidad_evaluadores = cantidad_evaluadores
    self.frecuencia_respuesta = frecuencia_respuesta
    self.estado_relacion = estado_relacion
    self.estado_proceso = estado_proceso

  def __str__(self):
    return f"Evaluación {self.id} - Enunciado: {self.enunciado}, Relación: {self.relacion}"
  


class Prompt:
  def __init__(self, id_prompt, descripcion, poblacion, nivel_ejecucion, plantilla):
    self.id_prompt = id_prompt
    self.descripcion = descripcion
    self.poblacion = poblacion
    self.nivel_ejecucion = nivel_ejecucion
    self.plantilla = plantilla

  def __str__(self):
    return f"Prompt {self.id_prompt} - Descripción: {self.descripcion}, Población: {self.poblacion}, Nivel de ejecución: {self.nivel_ejecucion}"




class Competencia:
  def __init__(self, id, descripcion, estado_activo):
    self.id = id
    self.descripcion = descripcion
    self.estado_activo = estado_activo
  
  def mostrar_info(self):
    return f"ID: {self.id}, Descripción: {self.descripcion}, Estado Activo: {self.estado_activo}"
 
class Fortaleza(Competencia):
  def __init__(self, id, descripcion, estado_activo, fortaleza):
    super().__init__(id, descripcion, estado_activo)
    self.fortaleza = fortaleza

  def mostrar_info(self):
    return f"{super().mostrar_info()}, Fortaleza: {self.fortaleza}"

class Brecha(Competencia):
  def __init__(self, id, descripcion, estado_activo, brecha):
    super().__init__(id, descripcion, estado_activo)
    self.brecha = brecha

  def mostrar_info(self):
    return f"{super().mostrar_info()}, Brecha: {self.brecha}"
  
class Supraconducta(Competencia):
  def __init__(self, id, descripcion, estado_activo, supraconducta):
    super().__init__(id, descripcion, estado_activo)
    self.supraconducta = supraconducta

  def mostrar_info(self):
    return f"{super().mostrar_info()}, Supraconducta: {self.supraconducta}"