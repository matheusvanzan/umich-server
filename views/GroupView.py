from .ScrudView import ScrudView
from ..models import Group
from ..forms import GroupForm


class GroupView(ScrudView):
    scrud_string = 'group'
    scrud_object = Group
    scrud_form = GroupForm