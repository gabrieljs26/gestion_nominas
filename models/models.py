from odoo import models, fields, api, exceptions

class Nomina(models.Model):
    _name = 'gestion.nomina'
    _description = 'Nómina de Empleado'
    _rec_name = 'empleado_id'

    # Campos definidos en el PDF 
    empleado_id = fields.Many2one('res.partner', string='Empleado', required=True)
    sueldo_base = fields.Monetary(string='Sueldo Base', required=True, currency_field='currency_id')
    fecha = fields.Date(string='Fecha', default=fields.Date.today, required=True)
    
    # Archivo PDF justificante 
    archivo_justificante = fields.Binary(string='Justificante Transferencia')
    nombre_archivo = fields.Char(string="Nombre Archivo")

    # Estado visualmente accesible 
    estado = fields.Selection([
        ('borrador', 'Redactada'),
        ('confirmada', 'Confirmada'),
        ('pagada', 'Pagada')
    ], string='Estado', default='borrador', tracking=True)

    # Relación One2many con líneas 
    linea_ids = fields.One2many('gestion.nomina.linea', 'nomina_id', string='Bonificaciones y Deducciones')

    # Cálculos IRPF 
    irpf_porcentaje = fields.Float(string='IRPF (%)')
    irpf_pagado = fields.Monetary(string='IRPF Pagado (€)', compute='_compute_irpf_pagado', store=True)
    
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    @api.depends('sueldo_base', 'linea_ids', 'irpf_porcentaje')
    def _compute_irpf_pagado(self):
        for record in self:
            # IRPF sobre base + bonificaciones (positivas)
            total_bonificaciones = sum(l.importe for l in record.linea_ids if l.importe > 0)
            base_imponible = record.sueldo_base + total_bonificaciones
            record.irpf_pagado = base_imponible * (record.irpf_porcentaje / 100)

class NominaLinea(models.Model):
    _name = 'gestion.nomina.linea'
    _description = 'Línea de Bonificación o Deducción'

    # Campos definidos en el PDF 
    nomina_id = fields.Many2one('gestion.nomina', string='Nómina')
    concepto = fields.Char(string='Concepto', required=True)
    importe = fields.Monetary(string='Importe Bruto', help="Positivo para bonificación, negativo para deducción")
    currency_id = fields.Many2one(related='nomina_id.currency_id')

class DeclaracionRenta(models.Model):
    _name = 'gestion.declaracion'
    _description = 'Declaración de la Renta Anual'

    # Campos definidos en el PDF 
    anio = fields.Integer(string='Año', required=True, default=lambda self: fields.Date.today().year)
    empleado_id = fields.Many2one('res.partner', string='Empleado', required=True)
    nomina_ids = fields.Many2many('gestion.nomina', string='Nóminas Incluidas')

    sueldo_bruto_total = fields.Monetary(string='Sueldo Bruto Total', compute='_compute_totales')
    impuestos_pagados_total = fields.Monetary(string='Total IRPF Pagado', compute='_compute_totales')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    @api.depends('nomina_ids')
    def _compute_totales(self):
        for record in self:
            total_sueldo = 0.0
            total_irpf = 0.0
            for nomina in record.nomina_ids:
                bonif = sum(l.importe for l in nomina.linea_ids if l.importe > 0)
                deduc = sum(l.importe for l in nomina.linea_ids if l.importe < 0)
                # Sueldo bruto total (Base + Bonificaciones - Deducciones)
                total_sueldo += (nomina.sueldo_base + bonif + deduc)
                total_irpf += nomina.irpf_pagado
            
            record.sueldo_bruto_total = total_sueldo
            record.impuestos_pagados_total = total_irpf

    # Restricción de seguridad: Datos con sentido 
    @api.constrains('nomina_ids', 'anio')
    def _check_nominas(self):
        for record in self:
            if len(record.nomina_ids) > 14: # 
                raise exceptions.ValidationError("No puede haber más de 14 nóminas en una declaración.")
            for nomina in record.nomina_ids:
                if nomina.fecha.year != record.anio: # 
                    raise exceptions.ValidationError(f"La nómina de {nomina.fecha} no pertenece al año {record.anio}")