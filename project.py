#!/usr/bin/env python

PRINT       = True
DB_NAME     = "ProjectDB"
ADMIN_PASS  = "admin"

RED         = "#F21A1A"
BLACK       = "#000000"
DARK_GREEN  = "#4A9445"
BG_COLOUR   = "#D6D8CB"

import wx, time, datetime, hashlib
import MySQLdb as mdb
import wx.grid as grid
import wx.lib.scrolledpanel as scrolled
from wx.lib.pubsub import Publisher

class DBFrame(wx.Frame):

    """
        Initialization
    """
    # set the dimensions for the basic elements
    FRAME_WIDTH        = 890
    FRAME_HEIGHT       = 490
    MENU_WIDTH         = 170
    BUTTON_HEIGHT      =  40
    V_MARGIN           =  10
    MENU_H_MARGIN      =  10
    MENU_GAP           =  10
    PANEL_TOP_MARGIN   =  30
    PANEL_BUTTON_WIDTH =  80
    PANEL_BUTTON_SPACE =  10
    PANEL_INPUT_HEIGHT =  30
    PANEL_INPUT_WIDTH  = 250
    PANEL_TEXT_WIDTH   =  80
    PANEL_V_SPACE      =  20
    PANEL_H_SPACE      =  10
    ADMIN_HASH         = "t\x9f\t\xba\xde\x8a\xcauV`\xee\xb1w\x92\xda\x88\x02\x18\xd4" +\
                         "\xfb\xdcN%\xfb\xec'\x9d\x7f\xe9\xf6]p"

    def __init__(self, parent = None, id = wx.ID_ANY):
        wx.Frame.__init__(self, parent, id,
                          "Introduction to Databases Final Project",
                          size=(self.FRAME_WIDTH, self.FRAME_HEIGHT))
        self.selected  = 'None'
        self.pick      = 0
        self.logged_in = False
        self.Admin     = False
        self.panel     = wx.Panel(self)
        self.panel.SetBackgroundColour(BG_COLOUR)
        self.init_window_elements()
        self.SetPosition((200, 100))
        Publisher().subscribe(self.usrLogin, ("user"))
        Publisher().subscribe(self.adminLogin, ("admin"))
        self.override_pass()

    # sets the password to ADMIN_PASS value at the top of the file
    def override_pass(self):
        m = hashlib.sha256()
        m.update(ADMIN_PASS)
        self.ADMIN_HASH = m.digest()

    # launches the window that gets the login info from the user
    def login(self):
        if len(self.GetChildren()) > 1: return
        frame = LoginFrame(self)
        frame.Show()

    # launches the window that to as for admin password
    def admin_login(self):
        frame = AdminLoginFrame(self)
        frame.Show()

    # recieves the login info and tries to connect to the database
    def usrLogin(self, msg):
        hostname, username, password = msg.data
        self.connect_to_database(hostname, username, password)

    # recieves the admin password and checks if it is correct
    def adminLogin(self, msg):
        m = hashlib.sha256()
        m.update(str(msg.data))
        if m.digest() == self.ADMIN_HASH:
            self.success('You are now logged in as Administrator.')
            self.Admin = True
        else:
            self.failure('the password provided was incorrect')

    # Initializes all the elements of the main window
    def init_window_elements(self):
        self.upper_menu_buttons = ['Customers', 'Reservations', 'Vacancies', 'Special Offers']
        self.lower_menu_buttons = ['Room Management', 'Hotel Management', 'VIPs', 'Debtors']
        self.menu_buttons       = self.upper_menu_buttons + self.lower_menu_buttons
        self.panel_buttons      = ['Add', 'Find', 'Update', 'Delete', 'Clear']

        self.values   = {}
        for menu in self.menu_buttons: self.values[menu] = {}

        self.calc_positions()
        self.sizes    = {'full' : self.PANEL_INPUT_SIZE,
                         'half' : self.PANEL_INPUT_HALF_SIZE,
                         'mini' : self.PANEL_INPUT_MINI_SIZE }
        self.needed   = {'needed' : [], 'opt' : [], 'auto' : [], 'now' : []}
        self.data     = {'bool'   : [], 'num' : [], 'text' : []}
        self.items    = {}
        self.tables   = {'Reservations'     : 'Reservation',
                         'Customers'        : 'Customer',
                         'Room Management'  : 'Room',
                         'Hotel Management' : 'Hotel',
                         'VIPs'             : 'VIPCustomer'}

        self.handlers = {'Reservations'     : self.create_reservations_panel,
                         'Customers'        : self.create_customers_panel,
                         'Vacancies'        : self.create_vacancies_panel,
                         'Special Offers'   : self.create_special_offers_panel,
                         'Room Management'  : self.create_room_management_panel,
                         'Hotel Management' : self.create_hotel_management_panel,
                         'Debtors'          : self.create_debtors_panel,
                         'VIPs'             : self.create_customers_panel }

        self.names    = {'Rid'              : 'Reserv. ID',
                         'id'               : 'Cust. ID',
                         'Payment Method'   : 'Payment',
                         'Res Date'         : 'Res. Date',
                         'Middle Name'      : 'Mid. Name',
                         'Municipality'     : 'Municip.',
                         'Mobile Phone'     : 'Mobile',
                         'Credit Card'      : 'CC',
                         'Hotel Name'       : 'Hotel'}
        self.create_menu_buttons()

    # Calculates and stores the positions of the right panel buttons
    def calc_positions(self):
        self.panel_pos = {}
        for i in range(len(self.panel_buttons)):
            pos = ((self.FRAME_WIDTH + self.MENU_WIDTH)/2 \
                   - self.PANEL_BUTTON_WIDTH*(len(self.panel_buttons)/2.0 - i) \
                   - self.PANEL_BUTTON_SPACE*((len(self.panel_buttons) - 1)/2.0 - i),
                   self.FRAME_HEIGHT - self.BUTTON_HEIGHT - self.V_MARGIN)
            self.panel_pos[self.panel_buttons[i]] = pos

        self.PANEL_BUTTON_SIZE     = (self.PANEL_BUTTON_WIDTH,  self.BUTTON_HEIGHT)
        self.PANEL_INPUT_SIZE      = (self.PANEL_INPUT_WIDTH,   self.PANEL_INPUT_HEIGHT)
        self.PANEL_INPUT_HALF_SIZE = (self.PANEL_INPUT_WIDTH/2, self.PANEL_INPUT_HEIGHT)
        self.PANEL_INPUT_MINI_SIZE = (50, self.PANEL_INPUT_HEIGHT)


    """
        Database connection
    """
    # Sets up the connection with the database.
    def connect_to_database(self, address, user, password, db = DB_NAME):
        try:
            conn = mdb.connect(address,user,password,db,sql_mode='STRICT_ALL_TABLES');
        except mdb.OperationalError:
            self.failure("the login information was incorrect")
        else:
            conn.autocommit(True)
            self.db = conn.cursor(mdb.cursors.DictCursor)
            self.success("Login Successful!")
            self.logged_in = True

    # Submits a query to the database and returns the result
    def query(self, query):
        if PRINT: print 'Submitting query:\n' + query + '\n'
        self.db.execute(query)
        return self.db.fetchall()

    
    """
        Element creation
    """
    # Creates the menu buttons on the left side of the frame.
    def create_menu_buttons(self):
        self.menu = {}
        for b_name in self.menu_buttons:
            v_offset = len(self.menu) * self.BUTTON_HEIGHT
            if b_name in self.lower_menu_buttons:
                v_offset += self.MENU_GAP
            b_pos    = (self.MENU_H_MARGIN, self.V_MARGIN + v_offset)
            b_size   = (self.MENU_WIDTH - 2*self.MENU_H_MARGIN, self.BUTTON_HEIGHT)
            self.menu[b_name] = wx.Button(self.panel, id = wx.ID_ANY, name = b_name,
                                          label = b_name, size = b_size, pos = b_pos)
            self.menu[b_name].SetBackgroundColour(RED)
            self.menu[b_name].SetForegroundColour(BLACK)
            self.menu[b_name].Bind(wx.EVT_BUTTON, self.onMenuButton)

    # Creates the appropriate right side panel corresponding to
    # the menu option pressed.
    def onMenuButton(self, event):
        selection = event.GetEventObject().GetName()
        if self.selected == selection: return
        if not self.logged_in:
            self.login()
            return
        if selection in self.lower_menu_buttons and not self.Admin:
            self.admin_login()
            return
        if self.selected != 'None':
            self.menu[self.selected].SetBackgroundColour(RED)

        self.store_values()
        self.clear_panel()
        self.selected = selection
        self.handlers[selection]()
        self.menu[selection].SetBackgroundColour(DARK_GREEN)
        self.restore_values()

    # Stores the current values of the active panel
    def store_values(self):
        if self.selected in self.tables:
            for key in self.keys():
                self.values[self.selected][key] = self.get(key)
        if self.selected == 'Special Offers': 
            self.values['Special Offers']['Beds'] = self.get('Beds')
        if self.selected == 'Vacancies':
            self.values['Vacancies']['Hotel Name'] = self.get('Hotel Name')
            self.values['Vacancies']['Beds']       = self.get('Beds')
            self.values['Vacancies']['Starting']   = self.get('Starting')
            self.values['Vacancies']['Max Price']  = self.get('Max Price')

    # Restoress the stored values into the active panel
    def restore_values(self):
        if len(self.values[self.selected]) == 0: return
        for key in self.keys():
            self.items[key].SetValue(self.values[self.selected][key])
        if self.selected == 'Special Offers':
            self.update_offers(None)
        if self.selected == 'Vacancies':
            self.update_vacancies(None)

    # Destroys all the right side panel elements
    def clear_panel(self):
        for key, item in self.items.iteritems(): item.Destroy()
        for arr in self.needed: self.needed[arr] = []
        for arr in self.data  : self.data[arr]   = []
        self.primary_keys = []
        self.items.clear()

    # Creates all the elements of the Reservations panel
    def create_reservations_panel(self):
        self.add_element('combo', 'Hotel Name',     3, 0, 0, 'full', 'needed', 'text', self.hotels())
        self.add_element('combo', 'Room No',        3, 1, 0, 'half', 'needed', 'num' )
        self.add_element('input', 'id',             3, 1, 1, 'half', 'needed', 'text')
        self.add_element('input', 'Rid',            3, 1, 2, 'half', 'auto'  , 'num' )
        self.add_element('input', 'Arrival',        3, 2, 0, 'half', 'needed', 'text')
        self.add_element('input', 'Departure',      3, 2, 1, 'half', 'needed', 'text')
        self.add_element('input', 'Cost',           3, 3, 0, 'half', 'needed', 'num' )
        self.add_element('input', 'Remainder',      3, 3, 1, 'half', 'needed', 'num' )
        self.add_element('combo', 'Payment Method', 3, 3, 2, 'half', 'needed', 'text',
                        ['', 'Cash', 'Credit Card'])
        self.add_element('input', 'Res Date',       3, 4, 0, 'full', 'now'   , 'text')
        self.items['Hotel Name'].Bind(wx.EVT_COMBOBOX, self.update_rooms_handler)
        self.primary_keys = ['Rid']
        self.create_panel_buttons()

    # Creates all the elements of the Customers panel
    def create_customers_panel(self):
        self.add_element('check', 'VIP',          2, 0, 0, 'mini', 'opt',    'bool', dx = 160)
        self.add_element('input', 'id',           2, 0, 0, 'half', 'needed', 'text')
        self.add_element('input', 'Middle Name',  2, 0, 1, 'full', 'opt',    'text')
        self.add_element('input', 'Name',         2, 1, 0, 'full', 'needed', 'text')
        self.add_element('input', 'Surname',      2, 1, 1, 'full', 'needed', 'text')
        self.add_element('input', 'State',        2, 2, 0, 'full', 'opt',    'text')
        self.add_element('input', 'City',         2, 2, 1, 'full', 'opt',    'text')
        self.add_element('input', 'Municipality', 2, 3, 0, 'full', 'opt',    'text')
        self.add_element('input', 'Zipcode',      2, 3, 1, 'half', 'opt',    'num' )
        self.add_element('input', 'Street',       2, 4, 0, 'full', 'opt',    'text')
        self.add_element('input', 'Street No',    2, 4, 1, 'half', 'opt',    'text')
        self.add_element('input', 'Phone',        2, 5, 0, 'half', 'opt',    'num' )
        self.add_element('input', 'Mobile Phone', 2, 5, 1, 'half', 'opt',    'num' )
        self.add_element('input', 'Email',        2, 6, 0, 'full', 'opt',    'text')
        self.add_element('input', 'Fax',          2, 6, 1, 'half', 'opt',    'num' )
        self.add_element('input', 'Credit Card',  2, 7, 0, 'full', 'opt',    'num' )
        self.add_element('input', 'Expires',      2, 7, 1, 'half', 'opt',    'text')
        self.primary_keys = ['id']
        self.create_panel_buttons()

    # Creates the vacanies panel
    def create_vacancies_panel(self):
        self.add_element('combo', 'Hotel Name', 3, 0, 0, 'full', 'opt', 'text', self.hotels(), dy=-10)
        self.add_element('combo', 'Beds',       3, 1, 0, 'half', 'opt', 'num',  dy=-10)
        self.add_element('input', 'Starting',   3, 1, 1, 'half', 'opt', 'text', dy=-10)
        self.add_element('input', 'Max Price',  3, 1, 2, 'half', 'opt', 'num' , dy=-10)
        self.items['Find'] = wx.Button(self.panel, id = wx.ID_ANY, name = 'Find', label = 'Find',
                                       size = self.PANEL_INPUT_HALF_SIZE, pos = self.pos3(0,2,0,-10))
        self.items['Find'].SetBackgroundColour(RED)
        self.items['Find'].SetForegroundColour(BLACK)
        self.items['Find'].Bind(wx.EVT_BUTTON, self.update_vacancies)
        self.items['Hotel Name'].Bind(wx.EVT_COMBOBOX, self.update_beds_handler)
        self.items['Starting'].SetValue(self.today())

    # Creates the table to display the vacancies
    def create_vacancies_table(self, res):
        if 'r_panel' in self.items: self.items['r_panel'].Destroy()
        start = self.str_to_date(self.get('Starting'))
        end = start + datetime.timedelta(days=26)
        rooms = self.get_rooms(self.get('Hotel Name'), self.get('Beds'), self.get('Max Price'))
        rooms.sort()
        table_height = (max(len(rooms),1) + 1)*25
        psize = (700, min(table_height, 16*25))
        gsize = (700, table_height)
        ppos  = (self.MENU_WIDTH, 120)
        self.items['r_panel'] = scrolled.ScrolledPanel(self, size = psize, pos = ppos)
        self.g = g = grid.Grid(self.items['r_panel'], size = gsize)
        g.CreateGrid(max(len(rooms),1), 26)
        g.SetMargins(-10,-10)
        g.SetGridLineColour(BLACK)
        g.SetRowLabelSize(50)
        g.SetColLabelSize(25)
        g.SetDefaultColSize(25)
        g.EnableEditing(False)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(g, 0, wx.EXPAND)
        self.items['r_panel'].SetSizer(vbox)
        self.items['r_panel'].SetAutoLayout(1)
        self.items['r_panel'].SetupScrolling(rate_y=25)
        
        # set the column labels to display the dates
        d = start
        for i in range(26):
            g.SetColLabelValue(i,str(d.day))
            d += datetime.timedelta(days=1)
        
        # set the row labels to display the rooms
        g.SetRowLabelValue(0,'-')
        for i in range(len(rooms)):
            g.SetRowLabelValue(i,str(rooms[i]))

        # make the unavailable dates red
        for i in range(len(res)):
            d = max(datetime.datetime.combine(res[i]['Arrival'], datetime.time()), start)
            dep = min(datetime.datetime.combine(res[i]['Departure'], datetime.time()), end)
            while d <= dep:
                g.SetCellBackgroundColour(rooms.index(res[i]['Room No']),
                                         (d - start).days, RED)
                d += datetime.timedelta(days=1)

        # event handling
        g.Bind(wx.EVT_MOUSEWHEEL, self.grid_handler)
        g.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.grid_vacancies_dclick)

    # returns all the room numbers in the given Hotel
    def get_rooms(self, hotel, beds, price):
        q = "SELECT `Room No` FROM Room\nWHERE `Hotel Name` = '%s' AND Beds = '%s'" % (hotel,beds)
        if price != '':
            if price.isdigit():
                q += " AND Price <= '%s'" % price
            else:
                self.failure('the Maximum Price entered is invalid.')
        q += '\nORDER BY `Room No` DESC'
        return [r['Room No'] for r in self.query(q)]

    # Updates the available beds for the selected hotel
    def update_beds_handler(self, event):
        res = self.query("SELECT DISTINCT Beds FROM Room, Hotel \n" +\
                         "WHERE Room.`Hotel Name` = Hotel.`Hotel Name` \n" +\
                         "AND Room.`Hotel Name` = '%s' " % self.get('Hotel Name'))
        self.items['Beds'].SetItems([str(b['Beds']) for b in res])
        if len(res) > 0: self.items['Beds'].SetValue(str(res[0]['Beds']))

    # Handler to display the room that was double clicked in the vacancies panel
    def grid_vacancies_dclick(self, event):
        hotel   = self.get('Hotel Name')
        room_no = self.g.GetRowLabelValue(event.GetRow())
        q = "SELECT * FROM Room \nWHERE `Hotel Name` = '%s' \nAND `Room No` = '%s'" % (hotel, room_no)
        res = self.query(q)
        self.store_values()
        self.menu['Vacancies'].SetBackgroundColour(RED)
        self.menu['Room Management'].SetBackgroundColour(DARK_GREEN)
        self.clear_panel()
        self.selected = 'Room Management'
        self.handlers['Room Management']()
        self.update_values(res)
        self.update_rooms_handler(None)

    # Finds and updates the vacancies into the vacancies panel
    def update_vacancies(self, event):
        if not self.valid_date(self.get('Starting')):
            self.failure('the date entered is invalid.')
            return ()
        start = self.str_to_date(self.get('Starting'))
        end = start + datetime.timedelta(days=27)
        hotel, beds = (self.get('Hotel Name'), self.get('Beds'))

        q = "SELECT Room.`Room No`, Arrival, Departure\n" +\
            "FROM Room, Reservation\n" +\
            "WHERE Room.`Hotel Name` = Reservation.`Hotel Name`\n" +\
            "AND Room.`Hotel Name` = '%s' AND Beds = '%s'\n" % (hotel, beds) +\
            "AND Room.`Room No` = Reservation.`Room No`\n" +\
            "AND ((Arrival <= '%s' AND Departure >= '%s')\n" % (start, start) +\
            "  OR (Arrival >= '%s' AND Departure <= '%s')\n" % (start, end) +\
            "  OR (Arrival <= '%s' AND Departure >= '%s'))" % (end,   end)
        if self.get('Max Price') != '':
            if self.get('Max Price').isdigit():
                q += "\nAND Price <= '%s'" % self.get('Max Price')
            else:
                self.failure('the Maximum Price entered is invalid.')
                return ()
        self.create_vacancies_table(self.query(q))

    # Creates the Special Offers panel
    def create_special_offers_panel(self):
        self.add_element('combo', 'Beds', 3, 0, 2, 'half', 'opt', 'num', self.get_beds(), dy = -10)
        self.items['Beds'].Bind(wx.EVT_COMBOBOX, self.update_offers)
        if 'Beds' not in self.values['Special Offers']: 
            self.create_offers_table(1)
        
    # Returns the available numbers of beds in the database
    def get_beds(self):
        res = self.query("SELECT DISTINCT Beds FROM Room ORDER BY Beds")
        return [str(b['Beds']) for b in res]
        
    # Handler to find the offers for the selected number of beds
    def update_offers(self, event):
        q = "SELECT * FROM Room\n" + \
            "WHERE Beds = '%s'\n" % self.get('Beds') + \
            "AND Price < 0.7 * \n" +\
            "    (SELECT avg(Price) FROM Room \n" +\
            "    GROUP BY Beds HAVING Beds = '%s')" % self.get('Beds') +\
            "\nORDER BY Price ASC"
        res = self.query(q)
        self.create_offers_table(max(len(res), 1))
        self.update_offers_values(res)

    # Creates the grid to display the debtors
    def create_offers_table(self, num_debtors):
        if 'r_panel' in self.items: self.items['r_panel'].Destroy()
        table_height = (num_debtors + 1)*25
        psize = (710, min(table_height, 16*25))
        gsize = (710, table_height)
        ppos  = (self.MENU_WIDTH, 70)
        self.items['r_panel'] = scrolled.ScrolledPanel(self, size=psize, pos = ppos)
        self.g = grid.Grid(self.items['r_panel'], size = gsize) 
        self.g.CreateGrid(num_debtors, 7)
        self.g.SetMargins(-10,-10)
        self.g.SetGridLineColour(BLACK)
        self.g.SetRowLabelSize(40)
        self.g.SetColLabelSize(25)
        self.g.EnableEditing(False)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.g, 0, wx.EXPAND)
        self.items['r_panel'].SetSizer(vbox)
        self.items['r_panel'].SetAutoLayout(1)
        self.items['r_panel'].SetupScrolling(rate_x = 25, rate_y=25)
        
        # set up the labels
        labels = ['Hotel Name', 'Room No', 'TV', 'AC', 'Suite', 'Balcony', 'Price']
        sizes  = [210, 90, 50, 50, 90, 90, 90]
        for i in range(7):
            self.g.SetColLabelValue(i,labels[i])
            self.g.SetColSize(i,sizes[i])

        # Alignment
        for i in range(num_debtors):
            self.g.SetCellAlignment(i,1,wx.ALIGN_RIGHT,wx.ALIGN_CENTRE)
            self.g.SetCellAlignment(i,3,wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)

        # event handling
        self.g.Bind(wx.EVT_MOUSEWHEEL, self.grid_handler)
        self.g.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.grid_offers_dclick)

    # Displays the given debtors in the debtors panel
    def update_offers_values(self, res):
        for i in range(len(res)):
            self.g.SetCellValue(i, 0, res[i]['Hotel Name'])
            self.g.SetCellValue(i, 1, str(res[i]['Room No']))
            self.g.SetCellValue(i, 6, str(res[i]['Price']))
            for pos, label in [(2,'TV'), (3,'AC'), (4,'Suite'), (5,'Balcony')]:
                if res[i][label] == 1: value = 'Yes'
                else                 : value = 'No'
                self.g.SetCellValue(i, pos, value)

    # Handler to display the customer that was double clicked in the customer panel
    def grid_offers_dclick(self, event):
        hotel   = self.g.GetCellValue(event.GetRow(), 0)
        room_no = self.g.GetCellValue(event.GetRow(), 1)
        if hotel == '': return
        q = "SELECT * FROM Room \nWHERE `Hotel Name` = '%s' \nAND `Room No` = '%s'" % (hotel, room_no)
        res = self.query(q)
        self.store_values()
        self.menu['Special Offers'].SetBackgroundColour(RED)
        self.menu['Room Management'].SetBackgroundColour(DARK_GREEN)
        self.clear_panel()
        self.selected = 'Room Management'
        self.handlers['Room Management']()
        self.update_values(res)
        self.update_rooms_handler(None)

    # Creates all the elements of the Room Management panel
    def create_room_management_panel(self):
        self.add_element('combo', 'Hotel Name', 3, 0, 0, 'full', 'needed', 'text', self.hotels())
        self.add_element('combo', 'Room No',    3, 1, 0, 'half', 'needed', 'num' )
        self.add_element('input', 'Price',      3, 1, 1, 'half', 'needed', 'num' )
        self.add_element('input', 'Beds',       3, 1, 2, 'half', 'needed', 'num' )
        self.add_element('check', 'TV',         3, 2, 0, 'mini', 'opt',    'bool')
        self.add_element('check', 'AC',         3, 2, 0, 'mini', 'opt',    'bool', dx = 80)
        self.add_element('check', 'Suite',      3, 2, 1, 'half', 'opt',    'bool')
        self.add_element('check', 'Balcony',    3, 2, 2, 'half', 'opt',    'bool')
        self.items['Hotel Name'].Bind(wx.EVT_COMBOBOX, self.update_rooms_handler)
        self.items['Room No'].Bind(wx.EVT_COMBOBOX, self.update_room_info)
        self.items['Room No'].SetEditable(True)
        self.primary_keys = ['Hotel Name', 'Room No']
        self.create_panel_buttons()

    # Creates all the elemets of the Hotel Management panel
    def create_hotel_management_panel(self):
        hotels = [''] + self.hotels()
        self.add_element('combo', 'Hotel Name',   2, 0, 0, 'full', 'needed', 'text', hotels)
        self.add_element('input', 'State',        2, 0, 1, 'full', 'needed', 'text')
        self.add_element('input', 'City',         2, 1, 0, 'full', 'needed', 'text')
        self.add_element('input', 'Municipality', 2, 1, 1, 'full', 'needed', 'text')
        self.add_element('input', 'Street',       2, 2, 0, 'full', 'needed', 'text')
        self.add_element('input', 'Street No',    2, 2, 1, 'half', 'needed', 'text')
        self.add_element('input', 'Phone',        2, 3, 0, 'half', 'needed', 'num' )
        self.add_element('input', 'Fax',          2, 3, 1, 'half', 'opt',    'num' )
        self.add_element('input', 'Email',        2, 4, 0, 'full', 'needed', 'text')
        self.add_element('check', 'Parking',      3, 5, 0, 'half', 'opt',    'bool')
        self.add_element('check', 'Restaurant',   3, 5, 1, 'half', 'opt',    'bool')
        self.add_element('check', 'WiFi',         3, 5, 2, 'half', 'opt',    'bool')
        self.add_element('check', 'Pool',         3, 6, 0, 'half', 'opt',    'bool')
        self.add_element('check', 'Gym',          3, 6, 1, 'half', 'opt',    'bool')
        self.items['Hotel Name'].Bind(wx.EVT_COMBOBOX, self.update_hotel_info)
        self.items['Hotel Name'].SetEditable(True)
        self.primary_keys = ['Hotel Name']
        self.create_panel_buttons()

    # Creates all the elements in the Debtors panel
    def create_debtors_panel(self):
        res = self.query("SELECT * FROM Debtor")
        self.create_debtors_table(max(len(res), 1))
        self.update_debtor_values(res)

    # Creates the grid to display the debtors
    def create_debtors_table(self, num_debtors):
        table_height = (num_debtors + 1)*25
        psize = (710, min(table_height, 18*25))
        gsize = (710, table_height)
        ppos  = (self.MENU_WIDTH, 10)
        self.items['r_panel'] = scrolled.ScrolledPanel(self, size=psize, pos = ppos)
        self.g = g = grid.Grid(self.items['r_panel'], size = gsize) 
        g.CreateGrid(num_debtors, 7)
        g.SetMargins(-10,-10)
        g.SetGridLineColour(BLACK)
        g.SetRowLabelSize(40)
        g.SetColLabelSize(25)
        g.EnableEditing(False)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.g, 0, wx.EXPAND)
        self.items['r_panel'].SetSizer(vbox)
        self.items['r_panel'].SetAutoLayout(1)
        self.items['r_panel'].SetupScrolling(rate_x = 25, rate_y=25)
        
        # set up the labels
        labels = ['ID', 'Surname', 'Name', 'VIP', 'Mobile', 'Phone', 'Debt']
        sizes  = [90, 140, 120, 50, 90, 90, 90]
        for i in range(7):
            g.SetColLabelValue(i,labels[i])
            g.SetColSize(i,sizes[i])

        # Alignment
        for i in range(num_debtors):
            g.SetCellAlignment(i,3,wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
            g.SetCellAlignment(i,6,wx.ALIGN_RIGHT,wx.ALIGN_CENTRE)

        # event handling
        g.Bind(wx.EVT_MOUSEWHEEL, self.grid_handler)
        g.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.grid_debtors_dclick)

    # Displays the given debtors in the debtors panel
    def update_debtor_values(self, res):
        for i in range(len(res)):
            self.g.SetCellValue(i, 0, res[i]['id'])
            self.g.SetCellValue(i, 1, res[i]['Surname'])
            self.g.SetCellValue(i, 2, res[i]['Name'])
            self.g.SetCellValue(i, 4, res[i]['Mobile Phone'])
            self.g.SetCellValue(i, 5, res[i]['Phone'])
            self.g.SetCellValue(i, 6, str(res[i]['Debt']))
            if res[i]['VIP'] == 1: vip = 'Yes'
            else                 : vip = 'No'
            self.g.SetCellValue(i, 3, vip)

    # Handler to redirect the mouse scroll to the ScrolledPanel
    def grid_handler(self, event):
        self.items['r_panel'].GetEventHandler().ProcessEvent(event)

    # Handler to display the customer that was double clicked in the customer panel
    def grid_debtors_dclick(self, event):
        cust_id = self.g.GetCellValue(event.GetRow(), 0)
        if cust_id == '': return
        q = "SELECT * FROM Customer WHERE id = '%s'" % cust_id
        res = self.query(q)
        self.menu['Debtors'].SetBackgroundColour(RED)
        self.menu['Customers'].SetBackgroundColour(DARK_GREEN)
        self.clear_panel()
        self.selected = 'Customers'
        self.handlers['Customers']()
        self.update_values(res)

    # Creates and adds the specified element to the right panel along with a static text if needed
    def add_element(self, element, name, dim, x, y, size, needed, data, options = [''], dx = 0, dy = 0):
        tpos, pos = self.get_pos(dim, x, y, dx, dy)
        ele_size  = self.sizes[size]
        label     = self.ui_name(name)
        self.needed[needed].append(name)
        self.data[data].append(name)
        if element == 'input':
            self.items[name + ' label'] = wx.StaticText(self.panel, -1, label + ':', tpos)
            self.items[name] = wx.TextCtrl(self.panel, -1, '', pos, ele_size)
        elif element == 'combo':
            self.items[name + ' label'] = wx.StaticText(self.panel, -1, label + ':', tpos)
            self.items[name] = wx.ComboBox(self.panel, -1, '', pos, ele_size, options)
            self.items[name].SetEditable(False)
        elif element == 'check':
            self.items[name] = wx.CheckBox(self.panel, -1, name, pos, ele_size)
        else:
            print 'Only input, combo and check elements are supported.'

    # Returns the position of the element on the right panel
    def get_pos(self, dim, x, y, dx, dy):
        if   dim == 2: return (self.tpos2(x,y,dx,dy), self.pos2(x,y,dx,dy))
        elif dim == 3: return (self.tpos3(x,y,dx,dy), self.pos3(x,y,dx,dy))
        else: print 'Only 2 or 3 elements per line are supported'

    # Adds the buttons at the bottom of the right panel
    def create_panel_buttons(self):
        for b in self.panel_buttons:
            self.items[b] = wx.Button(self.panel, id = wx.ID_ANY, name = b, label = b,
                                      size = self.PANEL_BUTTON_SIZE, pos = self.panel_pos[b])
            self.items[b].SetBackgroundColour(RED)
            self.items[b].SetForegroundColour(BLACK)
            self.items[b].Bind(wx.EVT_BUTTON, getattr(self, b.lower() + '_handler'))

    # Returns the position of a box on the right panel assuming 2 items per line
    def pos2(self, row, column, dx, dy):
        x = self.MENU_WIDTH + self.PANEL_H_SPACE + self.PANEL_TEXT_WIDTH + \
            (2*self.PANEL_H_SPACE + self.PANEL_TEXT_WIDTH + \
             self.PANEL_INPUT_WIDTH)*column
        y = self.PANEL_TOP_MARGIN + \
            (self.PANEL_INPUT_HEIGHT + self.PANEL_V_SPACE)*row
        return (x+dx,y+dy)

    # Returns the position of a static text element on the right panel
    # assuming 2 items per line
    def tpos2(self, row, column, dx, dy):
        x = self.MENU_WIDTH + self.PANEL_H_SPACE + \
            (2*self.PANEL_H_SPACE + self.PANEL_TEXT_WIDTH + \
             self.PANEL_INPUT_WIDTH)*column
        y = self.PANEL_TOP_MARGIN + 5 + \
            (self.PANEL_INPUT_HEIGHT + self.PANEL_V_SPACE)*row
        return (x+dx,y+dy)

    # Returns the position of a box on the right panel assuming 3 items per line
    def pos3(self, row, column, dx, dy):
        x = self.MENU_WIDTH + self.PANEL_H_SPACE + self.PANEL_TEXT_WIDTH + \
            (2*self.PANEL_H_SPACE + self.PANEL_TEXT_WIDTH + \
            self.PANEL_INPUT_WIDTH/2)*column
        y = self.PANEL_TOP_MARGIN + \
            (self.PANEL_INPUT_HEIGHT + self.PANEL_V_SPACE)*row
        return (x+dx,y+dy)

    # Returns the position of a static text element on the right panel
    # assuming 3 items per line
    def tpos3(self, row, column, dx, dy):
        x = self.MENU_WIDTH + self.PANEL_H_SPACE + \
            (2*self.PANEL_H_SPACE + self.PANEL_TEXT_WIDTH + \
            self.PANEL_INPUT_WIDTH/2)*column
        y = self.PANEL_TOP_MARGIN + 5 + \
            (self.PANEL_INPUT_HEIGHT + self.PANEL_V_SPACE)*row
        return (x+dx,y+dy)


    """
        Button handlers for the right panel buttons
    """
    # adds a new entry in the database
    def add_handler(self, event):
        # assert the data is valid
        for key in self.needed['auto'] + self.needed['now']:
            if self.get(key) != '':
                self.failure('%s must be left blank.' % self.ui_name(key))
                return
        for key in self.needed['needed']:
            if self.get(key) == '':
                self.failure('the field %s cannot be empty.' % self.ui_name(key))
                return
        for key in self.data['num']:
            if self.get(key) != '' and not self.get(key).isdigit():
                self.failure('the value for field %s is invalid.' % self.ui_name(key))
                return
            
        # make sure VIPs cannot be changed from the customers panel
        if self.selected == 'Customers' and self.get('VIP'):
            self.failure('VIPs can only be added through the VIP panel.')
            return

        # create the query
        q1 = 'INSERT INTO %s \n(' % self.tables[self.selected]
        q2 = ') \nVALUES \n('
        for key in self.keys():
            if key in self.needed['auto']:
                q1 += "`%s`, " % key
                q2 += "NULL, "
            if key in self.needed['now']:
                q1 += "`%s`, " % key
                q2 += "'%s', " % self.now()
            if key in self.needed['opt'] + self.needed['needed']:
                q1 += "`%s`, " % key
                if key in self.data['bool']:
                    if self.get(key): q2 += "'1', "
                    else:             q2 += "'0', "
                else:
                    q2 += "'%s', " % self.get(key)
        q = q1[:-2] + q2[:-2] + ')'
        
        # make the query
        try:
            self.query(q)
            self.success('Database entry successfully created.')
        except mdb.ProgrammingError:
            self.failure('could not add the entry to the database.')
        except mdb.OperationalError:
            self.failure('some of the values entered are invalid.')
        except mdb.IntegrityError:
            self.failure('could not add the entry to the database. ' + \
                         'Maybe that %s already exists.' % self.tables[self.selected])
            
    # Retrieves an entry from the database and displays it in the panel
    def find_handler(self, event):
        found = False
        q = 'SELECT * FROM %s \nWHERE ' % self.tables[self.selected]
        for key in self.data['num']:
            if self.get(key) == '': continue
            elif not self.get(key).isdigit():
                self.failure('the value for field %s is invalid.' % self.ui_name(key))
                return
            else:
                q += "`%s` = '%s' AND \n" % (key, self.get(key))
                found = True
        for key in self.data['text']:
            if self.get(key) != '':
                q += "`" + key + "` LIKE '%" + self.get(key) + "%' AND \n"
                found = True
        for key in self.data['bool']:
            if self.get(key):
                q += "`%s` = '1' AND \n" % key
                found = True
        if found: q = q[:-6]
        else:     q = 'SELECT * FROM %s' % self.tables[self.selected]
                
        # make the query
        res = self.query(q)
        self.update_values(res)

    # Updates the displayed values into the database
    def update_handler(self, event):
        # verify that the primary keys are provided
        for key in self.primary_keys:
            if self.get(key) == '':
                self.failure('the field %s cannot be blank.' % self.ui_name(key))
                return

        # make sure VIPs cannot be changed from the customers panel
        if self.selected == 'Customers':
            res = self.query("SELECT count(*) FROM VIPCustomer WHERE id = '%s'" % self.get('id'))
            if res[0]['count(*)'] > 0 or self.get('VIP'):
                self.failure('VIPs can only be modified through the VIP panel.')
                return
        
        # see if the entry exists
        q = 'SELECT count(*) FROM %s \nWHERE ' % self.tables[self.selected]
        for key in self.primary_keys:
            q += "`%s` = '%s' AND " % (key, self.get(key))
        q = q[:-5]
        res = self.query(q)
        if not res[0]['count(*)'] > 0:
            self.failure('that %s does not exist.' % self.tables[self.selected])
            return

        if not self.ask('Update values into the database?'): return

        # create the query
        q = 'UPDATE %s \nSET ' % self.tables[self.selected]
        for key in [k for k in self.keys() if k not in self.primary_keys]:
            if key in self.data['bool']:
                if self.get(key): q += "`%s` = '1', \n" % key
                else:             q += "`%s` = '0', \n" % key
            else:
                q += "`%s` = '%s', \n" % (key, self.get(key))
        q = q[:-3] + '\nWHERE '
        for key in self.primary_keys:
            q += "`%s` = '%s' AND " % (key, self.get(key))
        q = q[:-5]
        
        # update the database
        try:
            self.query(q)
            self.success('Database successfully updated.')
        except mdb.ProgrammingError:
            self.failure('could not add the values to the database.')
        except mdb.OperationalError:
            self.failure('some of the values entered were invalid.')
                
    # Deletes the displayed entry from the database
    def delete_handler(self, event):
        # verify that the primary keys are provided
        for key in self.primary_keys:
            if self.get(key) == '':
                self.failure('the field %s cannot be empty.' % self.ui_name(key))
                return
        
        # make sure VIPs cannot be changed from the customers panel
        if self.selected == 'Customers':
            res = self.query("SELECT count(*) FROM VIPCustomer WHERE id = '%s'" % self.get('id'))
            if res[0]['count(*)'] > 0:
                self.failure('VIPs can only be deleted through the VIP panel.')
                return

        # see if the entry exists
        q = 'SELECT count(*) FROM %s \nWHERE ' % self.tables[self.selected]
        for key in self.primary_keys:
            q += "`%s` = '%s' AND " % (key, self.get(key))
        q = q[:-5]
        res = self.query(q)
        if not res[0]['count(*)'] > 0:
            self.failure('that %s does not exist.' % self.tables[self.selected])
            return
        
        # ask for confirmation
        if not self.ask('Remove the entry from the database?'): return

        # make the query
        q = 'DELETE FROM %s \nWHERE ' % self.tables[self.selected]
        for key in self.primary_keys:
            q += "`%s` = '%s' AND " % (key, self.get(key))
        q = q[:-5]
        try:
            self.query(q)
            self.success('%s successfully deleted.' % self.tables[self.selected])
        except mdb.ProgrammingError:
            self.failure('could not remove the entry from the database.')
    
    # Clears all the fields in the right panel
    def clear_handler(self, event):
        for key in self.data['text'] + self.data['num']: self.items[key].SetValue('')
        for key in self.data['bool']:                    self.items[key].SetValue(False)

    # Updates the Room numbers of the selected hotel in the combo box
    def update_rooms_handler(self, event):
        if self.get('Hotel Name') == '': return
        res = self.query("SELECT `Room No` FROM Room \nWHERE `Hotel Name` = '%s'" \
                          % self.get('Hotel Name'))
        self.items['Room No'].SetItems([str(int(r['Room No'])) for r in res])

    # Updates the info for the selected room
    def update_room_info(self, event):
        if self.get('Hotel Name') == '' or self.get('Room No') == '': return
        res = self.query("SELECT * FROM Room \nWHERE `Hotel Name` = '%s' \nAND `Room No` = '%s'" \
                         % (self.get('Hotel Name'), self.get('Room No')))
        self.update_values(res)
        
    # Updates the info for the selected hotel
    def update_hotel_info(self, event):
        if self.get('Hotel Name') == '': return
        res = self.query("SELECT * FROM Hotel WHERE `Hotel Name` = '%s'" % self.get('Hotel Name'))
        self.update_values(res)

    # Updates the given values in the panel
    def update_values(self, values):
        if len(values) == 0:
            self.failure('could not find a %s with that info.' % self.tables[self.selected])
            return
        elif len(values) > 1:
            self.success('Found %d entries, showing the one of them.' % len(values))

        # update the values in the textboxes
        for key, value in values[self.pick % len(values)].iteritems():
            if key in self.data['bool']:
                if value == 1: self.items[key].SetValue(True)
                else:          self.items[key].SetValue(False)
            else:
                self.items[key].SetValue(str(value))
        self.pick += 1


    """
        Helper methods
    """
    # Returns the keys for all the form items in the right panel
    def keys(self):
        return [k for k in self.items if k not in self.panel_buttons and 'label' not in k]

    # Returns the value of the given right panel element
    def get(self, key):
        if key in self.items.keys(): return self.items[key].GetValue()
        else: print 'Internal Error: key does not exist.'

    # Asks the given question in a dialog box and returns the user choice
    def ask(self, question, caption = 'Are you sure?'):
        dlg = wx.MessageDialog(self.panel, question, caption, wx.YES_NO | wx.ICON_QUESTION)
        dlg.SetBackgroundColour(BG_COLOUR)
        result = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        return result

    # Displays a success dialog with the given message
    def success(self, message, caption = 'Success!'):
        dlg = wx.MessageDialog(self.panel, message, caption, wx.OK | wx.ICON_INFORMATION)
        dlg.SetBackgroundColour(BG_COLOUR)
        dlg.ShowModal()
        dlg.Destroy()

    # Displays a failure dialog with the given message
    def failure(self, message, caption = 'Error'):
        dlg = wx.MessageDialog(self.panel, 'Sorry, ' + message, 
                               caption, wx.OK | wx.ICON_EXCLAMATION)
        dlg.SetBackgroundColour(BG_COLOUR)
        dlg.ShowModal()
        dlg.Destroy()

    # Returns the UI name of the given element
    def ui_name(self, key):
        if key in self.names: return self.names[key]
        return key

    # Returns the names of the hotels that are now in the database
    def hotels(self):
        return [h['Hotel Name'] for h in self.query('SELECT `Hotel Name` FROM Hotel')]

    # Returns the current date and time
    def now(self): 
        return time.strftime("%Y-%m-%d %H:%M:%S")

    # Returns the current date
    def today(self):
        return time.strftime("%Y-%m-%d")

    # Returns the next day
    def next_date(self, date):
        return date + datetime.timedelta(days=1)

    # Converts the given string into a Date item
    def str_to_date(self, s):
        return datetime.datetime.strptime(s, "%Y-%m-%d")

    # Returns true if the string is in a valid date format
    def valid_date(self, s):
        try: time.strptime(s, '%Y-%m-%d')
        except ValueError: return False
        else:              return True

"""
    The frame that gets the login info from the user
"""
class LoginFrame(wx.Frame):
    def __init__(self, parent, id = -1):
        wx.Frame.__init__(self, parent, id, "Please connect to the database", size=(500, 150))
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(BG_COLOUR)
        self.SetPosition((300, 200))
        self.create_menu()

    # creates the log in menu
    def create_menu(self):
        self.name_l  = wx.StaticText(self.panel, -1, 'Username:', pos=(20,30))
        self.name    = wx.TextCtrl(self.panel, -1, '', pos=(100,25), size=(120,30))
        self.pswd_l  = wx.StaticText(self.panel, -1, 'Password:', pos=(240,30))
        self.pswd    = wx.TextCtrl(self.panel, -1, '', pos=(320,25), size=(120,30), style=wx.TE_PASSWORD)
        self.host_l  = wx.StaticText(self.panel, -1, 'Server:', pos=(20,90))
        self.host    = wx.TextCtrl(self.panel, -1, 'localhost', pos = (100,85), size=(120,30))
        self.connect = wx.Button(self.panel, id = wx.ID_ANY, name = 'Connect', 
                                 label = 'Connect...', size = (120,30), pos = (320,85))
        self.connect.SetBackgroundColour(RED)
        self.connect.SetForegroundColour(BLACK)
        self.connect.Bind(wx.EVT_BUTTON, self.onConnect)

    # sends the connection info back to the main frame and destroys the login frame
    def onConnect(self, event):
        msg = (self.host.GetValue(), self.name.GetValue(), self.pswd.GetValue())
        Publisher().sendMessage(("user"), msg)
        self.Destroy()

"""
    The frame that gets the administrator password from the user
"""
class AdminLoginFrame(wx.Frame):
    def __init__(self, parent, id = -1):
        wx.Frame.__init__(self, parent, id, "Administrator login", size=(400, 130))
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(BG_COLOUR)
        self.SetPosition((300, 200))
        self.create_menu()

    # creates the log in menu
    def create_menu(self):
        message = 'Please provide your administrator password:'
        self.info = wx.StaticText(self.panel, -1, message, pos=(30,25))
        self.pswd = wx.TextCtrl(self.panel, -1, '', pos = (30,70), size=(150,30), style=wx.TE_PASSWORD)
        self.conn = wx.Button(self.panel, id = wx.ID_ANY, name = 'Connect', 
                              label = 'Connect...', pos = (220,70), size = (150,30))
        self.conn.SetBackgroundColour(RED)
        self.conn.SetForegroundColour(BLACK)
        self.conn.Bind(wx.EVT_BUTTON, self.onConnect)

    # sends the connection info back to the main frame and destroys the login frame
    def onConnect(self, event):
        Publisher().sendMessage(("admin"), self.pswd.GetValue())
        self.Destroy()


# So it begins
if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = DBFrame().Show()
    app.MainLoop()
