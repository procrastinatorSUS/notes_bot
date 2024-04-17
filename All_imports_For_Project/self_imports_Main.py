from Process_And_Handlers.AddNote_Command import *
from Process_And_Handlers.AddNote_Fill_Process import *
from Process_And_Handlers.MyNotes_DelNone_Commands import *
from Process_And_Handlers.Start_Help_Commands import *
from Process_And_Handlers.StopNote_Cancel_Commands import *


from utils.commands import set_commands
from utils.filter_check_id import CheckDatabaseLess, CheckDatabaseMore, CheckNotifications, CheckForMinute
from utils.generator_buttons import dict_days_31,dict_months, dict_hours
