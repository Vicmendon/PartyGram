from django import template
from midia.models import Foto, Video  # Importe as classes Foto e Video

register = template.Library()

@register.filter(name='instance_of')
def instance_of(value, arg):
    """Retorna True se o valor for uma instância da classe passada como argumento"""
    # Comparar com as classes Foto ou Video
    if arg == 'Foto':
        return isinstance(value, Foto)
    elif arg == 'Video':
        return isinstance(value, Video)
    return False