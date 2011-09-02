{
    'name': 'Localization for Argentina',
    'version': '1.0',
    'author': 'Thymbra - Torre de Hanoi',
    'category': 'Localisation/America',
    'description': """
        Modelo de Localización para Argentina
        Incluye:
            - Plan Contable
            - Provincias
            - Impuestos básicos
            - Denominaciones de Partners y Contactos
            - Moneda ( Peso Argentino )

        Autor : Luis Falcon

        www.thymbra.com

        Encoding : UTF-8
        Licencia : GPL
    """,
    'depends': [
        'base',
        'account',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'res_country_states.xml',
        'res_partner_title.xml',
    ],
    'active': False,
}
