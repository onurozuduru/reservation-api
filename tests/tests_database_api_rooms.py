import unittest, sqlite3
from reservation import database

#Path to the database file, different from the deployment db
#Please run setup script first to make sure test database is OK.
DB_PATH = "database/test_tellus.db"
ENGINE = database.Engine(DB_PATH)

#CONSTANTS DEFINING DIFFERENT USERS AND USER PROPERTIES
NEW_USER = "newuser"
USER_DICT_CORRECT_DATA = {'isadmin': 0,
                          'password': 'test_pass',
                          'firstname': 'firstname0',
                          'lastname': 'lastname0',
                          'email': 'john@example.com',
                          'contactnumber': '69696969'}
EXSISTING_USER = "para"
NOT_EXSISTING_USER = "CrazyBoy95"
INITIAL_SIZE_USER = 3

ROOMNAME1 = 'Stage'
ROOMNAME2 = 'Chill'
WRONG_ROOMNAME = 'Vodka'

BOOKING1 = {'roomname': 'Stage',
            'date': '20170301',
            'time': '1000',
            'firstname': 'Onur',
            'lastname': 'Ozuduru',
            'email': 'onur.ozuduru@ee.oulu.fi',
            'contactnumber': '0411311911'}
BOOKING2 = {'roomname': 'Chill',
            'date': '2017035',
            'time': '1200',
            'firstname': 'Paramartha',
            'lastname': 'Narendradhipa',
            'email': 'paramartha.n@ee.oulu.fi',
            'contactnumber': '0417511944'}
INITIAL_SIZE_BOOKING = 2


class DBAPITestCase(unittest.TestCase):
    '''
    Test cases for the database API.
    It includes test cases for User, Room and Booking.
    '''
    #INITIATION METHODS
    def setUp(self):
        '''
        Populates the database
        '''
        #Creates a Connection instance to use the API
        self.connection = ENGINE.connect()

    def tearDown(self):
        '''
        Close underlying connection.
        '''
        self.connection.close()

    def test_users_table_created(self):
        '''
        Checks that the table initially contains 3 users (check
        tellus_data_dump.sql). NOTE: Do not use Connection instance but
        call directly SQL.
        '''
        print '('+self.test_users_table_created.__name__+')', \
              self.test_users_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM Users'
        #Connects to the database.
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            users = cur.fetchall()
            #Assert
            self.assertEquals(len(users), INITIAL_SIZE_USER)

    #TESTS FOR Users
    def test_add_user(self):
        '''
        Test that I can add new user
        '''
        print '(' + self.test_add_user.__name__ + ')', \
            self.test_add_user.__doc__
        username = self.connection.add_user(NEW_USER, USER_DICT_CORRECT_DATA)
        self.assertIsNotNone(username)
        self.assertEquals(username, NEW_USER)
        #Check that user is really created
        # Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = "SELECT * FROM Users WHERE username = '%s'" % NEW_USER
        # Connects to the database.
        con = self.connection.con
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Execute main SQL Statement
            cur.execute(query)
            users = cur.fetchall()
            # Assert
            self.assertEquals(len(users), 1)

    def test_add_existing_user(self):
        '''
        Test that I cannot add two users with the same username
        '''
        print '(' + self.test_add_existing_user.__name__ + ')', \
            self.test_add_existing_user.__doc__
        username = self.connection.add_user(EXSISTING_USER, USER_DICT_CORRECT_DATA)
        self.assertIsNone(username)

    def test_delete_user(self):
        '''
        Test that the user "para" is deleted
        '''
        print '(' + self.test_delete_user.__name__ + ')', \
            self.test_delete_user.__doc__
        resp = self.connection.delete_user(EXSISTING_USER)
        self.assertTrue(resp)
        # Check that the user has been really deleted from db
        # Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = "SELECT * FROM Users WHERE username = '%s'" % EXSISTING_USER
        # Connects to the database.
        con = self.connection.con
        with con:
            # Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Provide support for foreign keys
            cur.execute(keys_on)
            # Execute main SQL Statement
            cur.execute(query)
            users = cur.fetchall()
            # Assert
            self.assertEquals(len(users), 0)

    def test_delete_user_noexistingnickname(self):
        '''
        Test delete_user with the non-existing user "CrazyBoy95"
        '''
        print '(' + self.test_delete_user_noexistingnickname.__name__ + ')', \
            self.test_delete_user_noexistingnickname.__doc__
        # Test with an existing user
        resp = self.connection.delete_user(NOT_EXSISTING_USER)
        self.assertFalse(resp)

    # TESTS FOR Bookings
    def test_bookings_table_created(self):
        '''
        Checks that the table initially contains 2 bookings (check
        tellus_data_dump.sql). NOTE: Do not use Connection instance but
        call directly SQL.
        '''
        print '('+self.test_bookings_table_created.__name__+')', \
              self.test_bookings_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM Bookings'
        #Connects to the database.
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            users = cur.fetchall()
            #Assert
            self.assertEquals(len(users), INITIAL_SIZE_BOOKING)

    def test_get_bookings(self):
        '''
        Test that get_bookings work correctly without roomname
        '''
        print '(' + self.test_get_bookings.__name__ + ')', self.test_get_bookings.__doc__
        bookings = self.connection.get_bookings()
        # Check that the size is correct
        self.assertEquals(len(bookings), INITIAL_SIZE_BOOKING)
        # Iterate through bookings and check if the bookings with ROOMNAME1 and
        # ROOMNAME2 are correct:
        for booking in bookings:
            if booking['roomname'] == ROOMNAME1:
                self.assertEquals(len(booking), 7)
                self.assertDictContainsSubset(booking, BOOKING1)
            elif booking['roomname'] == ROOMNAME2:
                self.assertEquals(len(booking), 7)
                self.assertDictContainsSubset(booking, BOOKING2)

    def test_get_bookings_specific_roomname(self):
        '''
        Get all bookings for roomname "Chill".
        Check that it includes information for BOOKING2

        '''
        print '(' + self.test_get_bookings_specific_roomname.__name__ + ')', \
            self.test_get_bookings_specific_roomname.__doc__
        bookings = self.connection.get_bookings(roomname=ROOMNAME2)
        # Check length of the array is correct
        self.assertEquals(len(bookings), 1)
        # Check that data is correct
        self.assertDictContainsSubset(bookings[0], BOOKING2)

    def test_get_bookings_wrong_roomname(self):
        '''
        Test get_bookings with wrong roomname "Vodka"
        '''
        print '(' + self.test_get_bookings_wrong_roomname.__name__ + ')', \
            self.test_get_bookings_wrong_roomname.__doc__
        bookings = self.connection.get_bookings(roomname=WRONG_ROOMNAME)
        # Check length of the array is correct
        self.assertListEqual(bookings, [])

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()