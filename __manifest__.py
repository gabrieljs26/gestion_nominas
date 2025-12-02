{
    'name': "Gestión de Nóminas SGE",
    'summary': "Gestión de nóminas y declaración de la renta (Tarea 12)",
    'description': """
        Módulo para gestionar:
        - Nóminas de empleados (Sueldo base + Bonificaciones - Deducciones) 
        - Cálculo automático de IRPF 
        - Estados de la nómina (Redactada, Confirmada, Pagada) 
        - Declaración de la renta anual (Máx 14 nóminas) 
    """,
    'author': "Gabriel Gutierrez",
    'category': 'Human Resources',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}