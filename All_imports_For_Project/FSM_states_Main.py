from aiogram.fsm.state import default_state, State, StatesGroup


class FSMNoteForm(StatesGroup):
    note_text = State()
    note_month = State()
    note_days = State()
    note_hours = State()
    note_minute = State()
class FSMNoteDel(StatesGroup):
    note_id = State()