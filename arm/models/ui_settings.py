from models.arm_models import ARMModel
from models.db_setup import db


class UISettings(ARMModel):
    """
    ARM Database Model - UISettings

    Holds various settings related to the user interface, such as whether to use icons,
    whether to save remote images, the Bootstrap skin, the language preference, refresh intervals
    for index and notifications, and a database limit setting.

    Database Table:
        ui_settings

    Attributes:
        id (int): The unique identifier for the UI settings entry.
        use_icons (bool): Indicates whether to use icons in the user interface.
        save_remote_images (bool): Indicates whether to save remote images.
        bootstrap_skin (str): The selected Bootstrap skin for styling.
        language (str): The language preference for the user interface.
        index_refresh (int): The refresh interval for the index page, in milliseconds.
        database_limit (int): Limit for database entries to display.
        notify_refresh (int): The refresh interval for notifications, in milliseconds

    Relationships:
        None.
    """
    __tablename__ = 'ui_settings'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    use_icons = db.Column(db.Boolean)
    save_remote_images = db.Column(db.Boolean)
    bootstrap_skin = db.Column(db.String(64))
    language = db.Column(db.String(4))
    index_refresh = db.Column(db.Integer)
    database_limit = db.Column(db.Integer)
    notify_refresh = db.Column(db.Integer)

    def __init__(self, use_icons: bool = None, save_remote_images: bool = None,
                 bootstrap_skin: str = "", language: str = "", index_refresh: int = 2000,
                 database_limit: int = 0, notify_refresh: int = 2000):
        self.use_icons = use_icons
        self.save_remote_images = save_remote_images
        self.bootstrap_skin = bootstrap_skin
        self.language = language
        self.index_refresh = index_refresh
        self.database_limit = database_limit
        self.notify_refresh = notify_refresh
