import sqlite3

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.widget import Widget



class MainWindow(Widget):
    pass

class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_good = True
        self.validinfo=()
        self.thisone=""
        self.attendantfound = False
        self.cpassw=""
        self.thiscust=""
        self.adminpass="123456789"


    def getallatt(self):
        conn = sqlite3.connect('primebank.db')
        c = conn.cursor()
        c.execute("""SELECT rowid,fname,lname FROM attendants 
                    """)
        allatt=c.fetchall()
        conn.commit()
        conn.close()
        return allatt

    def gethisatt(self):
        conn = sqlite3.connect('primebank.db')
        c = conn.cursor()
        c.execute("""SELECT rowid,fname,lname FROM attendants 
                    ORDER BY rowid DESC
                    """)
        thisatt=c.fetchone()
        conn.commit()
        conn.close()
        return thisatt

    def registatt(self):
        self.current = "registeratt"

    def validate_att_reg(self):
        tatt_fname = self.ids.att_first
        tatt_mname = self.ids.att_sec
        tatt_lname = self.ids.att_third
        tatt_gen = self.ids.att_gen
        tatt_yob = self.ids.att_yob
        tatt_id = self.ids.att_id
        tatt_passw = self.ids.att_passw
        tatt_realpassw = self.ids.att_conf_passw

        att_fname=tatt_fname.text
        if att_fname=="":
            self.ids.validate_fname.text="Please Enter Your First Name"
            fname_good=False
        else:
            self.ids.validate_fname.text = " "
            fname_good=True
        att_mname=tatt_mname.text
        if att_mname == "":
            self.ids.validate_mname.text = "Please Enter Your SecondName"
            mname_good=False
        else:
            self.ids.validate_mname.text = " "
            mname_good=True
        att_lname=tatt_lname.text
        if att_lname == "":
            self.ids.validate_lname.text = "Please Enter Your Last Name"
            lname_good=False
        else:
            self.ids.validate_lname.text = " "
            lname_good=True
        att_gen=tatt_gen.text
        if att_gen == "":
            self.ids.validate_gen.text = "Please Enter Gender"
            gen_good=False
        else:
            self.ids.validate_gen.text = " "
            gen_good=True
        att_yob=tatt_yob.text
        if att_yob == "":
            self.ids.validate_yob.text = "Please Enter Year of Birth"
            yob_good=False
        else:
            self.ids.validate_passwconf.text = " "
            yob_good=True
        att_id=tatt_id.text
        if att_id == "":
            self.ids.validate_id.text = "Please Enter Your Id"
            id_good = False
        else:
            self.ids.validate_id.text = " "
            id_good = True
        att_passw=tatt_passw.text
        if att_passw=="":
            self.ids.validate_passw.text="Password Cannot Be Empty"
            passw_good = False
        else:
            self.ids.validate_passw.text = " "
            passw_good = True
        att_realpassw=tatt_realpassw.text
        if att_realpassw=="":
            self.ids.validate_passwconf.text = "Confirm Your Password"
            realpassw_good = False
        else:
            self.ids.validate_passwconf.text = " "
            realpassw_good= True

        if att_passw==att_realpassw:
            passw_good=True
            self.ids.validate_passwconf.text = " "
        else:
            passw_good=False
            self.ids.validate_passwconf.text = "Passwords Do Not Match"

        if fname_good and mname_good and lname_good and gen_good and yob_good and id_good and passw_good and realpassw_good:
            self.all_good=True
        else:
            self.all_good=False

        if self.all_good==True:
            continu=True
            self.ids.attregist_feedback.text="The Information Is All Valid"
            self.ids.togglesub.disabled=False
        else:
            continu=False
            self.ids.attregist_feedback.text="Validate Information"
            self.ids.togglesub.disabled = True


        if continu:
            fname=att_fname
            mname=att_mname
            lname=att_lname
            gen=att_gen
            yob=att_yob
            id=att_id
            realpassw=att_realpassw
            self.validinfo=(fname,mname,lname,gen,yob,id,realpassw)

    def get_info(self):
        return self.validinfo

    def validate_me(self):
        conn = sqlite3.connect('primebank.db')
        c = conn.cursor()
        c.execute("""SELECT rowid FROM attendants  
                            """)
        empidtext = self.ids.attval.text
        empidtext=int(empidtext)
        empidsindb=c.fetchall()
        for eachempidindb in empidsindb:
            for empidindb in eachempidindb:
                if empidindb==empidtext:
                    self.attendantfound=True
                    thisatt=empidindb
                    conn = sqlite3.connect('primebank.db')
                    c = conn.cursor()
                    c.execute("""SELECT rowid,fname,lname,passw,yob FROM attendants 
                                        WHERE rowid Like (?)
                                        """,str(thisatt))
                    self.thisone = c.fetchone()
                    conn.commit()
                    conn.close()
        if self.attendantfound:
            self.ids.attpassval.disabled=False
            self.ids.attval.disabled=True
            self.ids.attpassval.focus=True

        else:
            self.ids.employeevalidation.text = "Not Found"

    def loginagain(self):
        self.refreshlogin()

    def refreshlogin(self):
        self.ids.loginbutton.disabled = True
        self.ids.attpassval.disabled = True
        self.ids.attval.disabled = False
        self.ids.attpassval.text=""
        self.ids.attval.text=""
        self.ids.employeevalidation=""
        self.ids.attvaalinstr.text="Enter Required Details"
        self.ids.attpasswarning.text=""
        self.ids.loginbutton.disabled = True

    def validatepass(self):
        validation=self.ids.attpasswarning
        passtext=self.ids.attpassval
        password=self.thisone[3]
        if not passtext.text==password:
            validation.text="Wrong Password"
        else:
            validation.text = " "
            self.ids.loginbutton.disabled=False
            attid = self.thisone[0]
            attname = self.thisone[1] + "  " + self.thisone[2]
            attage = 2021 - int(self.thisone[4])
            self.ids.ide.text = str(attid)
            self.ids.nam.text = attname
            self.ids.ag.text = str(attage)

    def custphot(self,pic):
        try:
            picust=self.ids.piccus
            img=pic[0]
            picust.source=img
            self.ids.photbutt.disabled=False
        except:
            pass

    def customersp(self):
        try:
            self.customerphoto=self.ids.piccus.source
            self.ids.photoinst.text=""
            self.ids.photobox.remove_widget(self.ids.chosenpic)
            self.ids.photbutt.disabled=True
        except:
            pass


    def custfnameval(self):
        fnameval=self.ids.tcustfname
        if not fnameval.text =="":
            self.ids.tcustfname.disabled=True
            self.ids.tcustmname.disabled=False
            self.ids.tcustmname.focus=True
            self.ids.lstate.text = "FirstName Recieved"
        else:
            self.ids.lstate.text="No FirstName"

    def custmnameval(self):
        mnameval=self.ids.tcustmname
        if not mnameval.text =="":
            self.ids.tcustmname.disabled=True
            self.ids.tcustlname.disabled=False
            self.ids.tcustlname.focus=True
            self.ids.lstate.text = "SecondName Recieved"
        else:
            self.ids.lstate.text="No SecondName"

    def custlnameval(self):
        lnameval=self.ids.tcustlname
        if not lnameval.text =="":
            self.ids.tcustlname.disabled=True
            self.ids.tcustgender.disabled=False
            self.ids.tcustgender.focus=True
            self.ids.lstate.text = "SurName Recieved"
        else:
            self.ids.lstate.text="No Surname"

    def custgenval(self):
        genval=self.ids.tcustgender
        if not genval.text =="":
            self.ids.tcustgender.disabled=True
            self.ids.tcustbirthyear.disabled=False
            self.ids.tcustbirthyear.focus=True
            self.ids.lstate.text = "Gender Recieved"
        else:
            self.ids.lstate.text="No Gender"

    def custbyearval(self):
        byearval=self.ids.tcustbirthyear
        if not byearval.text =="":
            self.ids.tcustbirthyear.disabled=True
            self.ids.tcustid.disabled=False
            self.ids.tcustid.focus=True
            self.ids.lstate.text = "Year Recieved"
        else:
            self.ids.lstate.text="No Year"

    def custidval(self):
        idval = self.ids.tcustid
        if not idval.text == "":
            self.ids.tcustid.disabled = True
            self.ids.tcustphone.disabled = False
            self.ids.tcustphone.focus = True
            self.ids.lstate.text = "ID Recieved"
        else:
            self.ids.lstate.text = "No ID"
    def custpval(self):
        phoneval = self.ids.tcustphone
        if not phoneval.text == "":
            self.ids.tcustphone.disabled = True
            self.ids.tcustemail.disabled = False
            self.ids.tcustemail.focus = True
            self.ids.lstate.text = "PhoneNo Recieved"
        else:
            self.ids.lstate.text = "No PhoneNo"

    def custemval(self):
        emailval = self.ids.tcustemail
        if not emailval.text == "":
            self.ids.tcustemail.disabled = True
            self.ids.tcustpassword.disabled = False
            self.ids.tcustpassword.focus = True
            self.ids.lstate.text = "Email Recieved"
        else:
            self.ids.lstate.text = "No Email"

    def custpassval(self):
        passval = self.ids.tcustpassword
        if not passval.text == "":
            self.ids.tcustpassword.disabled = True
            self.ids.lstate.text = "Password Recieved"
            self.ids.buttsub.disabled=False
        else:
            self.ids.lstate.text = "No Password"

    def custreg(self):
        transaction="Customer Registration"
        custregphoto = self.ids.piccus.source
        custregfname = self.ids.tcustfname.text
        custregmname = self.ids.tcustmname.text
        custreglname = self.ids.tcustlname.text
        custreggen = self.ids.tcustgender.text
        custregyear = self.ids.tcustbirthyear.text
        custregid = self.ids.tcustid.text
        custregphone = self.ids.tcustphone.text
        custregemail = self.ids.tcustemail.text
        custregpassword = self.ids.tcustpassword.text
        custregatt =self.thisone[0]
        custreginputtuple=(custregfname,custregmname,custreglname,custreggen,custregyear,custregid,custregphoto,custregphone,custregemail,custregpassword,custregatt)
        conn = sqlite3.connect('primebank.db')
        c = conn.cursor()
        c.execute("""INSERT INTO customers 
                                VALUES(?,?,?,?,?,?,?,?,?,?,?)""", custreginputtuple)
        c.execute("""SELECT rowid FROM customers ORDER BY rowid DESC """)
        custids = c.fetchone()
        thiscustid = custids[0]
        trantuple=(transaction,thiscustid,custregatt)
        c.execute("""INSERT INTO transactions 
                                        VALUES(?,?,?)""",trantuple )
        c.execute("""SELECT rowid,transaction_type,customer,attendant FROM transactions ORDER BY rowid DESC """)
        thistrans = c.fetchone()
        self.ids.lstate.text=" Customer Added!"
        self.ids.buttsub.disabled = True
        conn.commit()
        conn.close()
        self.refreshcustreg()
        self.__init__()


    def refreshcustreg(self):
        self.ids.piccus.source=""
        self.ids.tcustfname.text=""
        self.ids.tcustfname.disabled = False
        self.ids.tcustmname.text=""
        self.ids.tcustmname.disabled=True
        self.ids.tcustlname.text=""
        self.ids.tcustlname.disabled = True
        self.ids.tcustgender.text=""
        self.ids.tcustgender.disabled = True
        self.ids.tcustbirthyear.text=""
        self.ids.tcustbirthyear.disabled = True
        self.ids.tcustid.text=""
        self.ids.tcustid.disabled = True
        self.ids.tcustphone.text=""
        self.ids.tcustphone.disabled = True
        self.ids.tcustemail.text=""
        self.ids.tcustemail.disabled = True
        self.ids.tcustpassword.text=""
        self.ids.tcustpassword.disabled = True
        self.ids.lstate.text = ""
        self.ids.buttsub.disabled=True
        self.ids.photbutt.disabled = True
        self.ids.photoinst.text="Choose Customer Photo"
        try:
            self.ids.photobox.add_widget(self.ids.chosenpic)
        except:
            pass
    def add_attendant(self):
        self.ids.togglesub.disabled = True
        if self.all_good==False:
            self.validate_att_reg()
        else:
            inputtuple=self.validinfo
            conn= sqlite3.connect('primebank.db')
            c = conn.cursor()
            c.execute("""INSERT INTO attendants 
                        VALUES(?,?,?,?,?,?,?)""",inputtuple)
            conn.commit()
            conn.close()
        self.ids.att_first.text=""
        self.ids.att_sec.text = ""
        self.ids.att_third.text = ""
        self.ids.att_gen.text = ""
        self.ids.att_yob.text = ""
        self.ids.att_id.text = ""
        self.ids.att_passw.text = ""
        self.ids.att_conf_passw.text=""
        curratt=self.gethisatt()
        myfirstname=curratt[1]
        mylastname=curratt[2]
        myemployeeid=curratt[0]
        self.current="RegisterAttendantSuccess"
        mydetailslayout=self.ids.mydetails
        mynamelabel1=Label(text=f'Successfully Registered as  {myfirstname} {mylastname}',size_hint=(1,.2),color=(0,1,0))
        mynamelabel2 = Label(text=f'Your Attendant ID is {myemployeeid}', size_hint=(1,.2),color=(0,0,1))
        mydetailslayout.add_widget(mynamelabel1)
        mydetailslayout.add_widget(mynamelabel2)
        mydetailslayout.add_widget(Label(size_hint=(1,.6)))

    def searchcus(self):
        fullname=self.ids.dfullname
        sex=self.ids.dsex
        age=self.ids.dage
        email=self.ids.demail
        phone=self.ids.dphone
        pc=self.ids.cuspic
        idno=self.ids.search
        conn = sqlite3.connect('primebank.db')
        c = conn.cursor()
        c.execute("""SELECT rowid,fname,mname,lname,gen,yob,id,custphoto,phone,email,secret FROM customers
                                                    """)
        custlist = c.fetchall()
        for onecust in custlist:
            if onecust[6]==idno.text:
                fullname.text=onecust[1] + " " + onecust[2] + " " + onecust[3]
                if onecust[4]=="M":
                    sex.text="Male"
                else:
                    sex.text="Female"
                age.text=str(2021-onecust[5])
                email.text = onecust[9]
                phone.text = onecust[8]
                pc.source = onecust[7]
                self.cpassw=onecust[10]
                self.thiscust=onecust[0]
        conn.commit()
        conn.close()



    def valcus(self):
        ps=self.ids.verpass
        pa=ps.text
        if pa==self.cpassw:
            self.ids.vermessage.text="VERIFIED"
            transaction = "Verification SUCCESSFUL"
        else:
            self.ids.vermessage.text = "WRONG PASSWORD"
            transaction = "Verification FAILED"

        vertuple=[transaction,self.thiscust,self.thisone[0]]

        conn = sqlite3.connect('primebank.db')
        c = conn.cursor()
        c.execute("""INSERT INTO transactions 
                                VALUES(?,?,?)""",vertuple )
        conn.commit()
        conn.close()
    def validatepassadmin(self):
        if self.ids.attadmnval.text==self.adminpass:
            self.ids.adminpasswarning.text="Correct"
            self.ids.valadmin.disabled=False
        else:
            self.ids.adminpasswarning.text = "Incorrect"
            self.ids.valadmin.disabled = True






class AttendantsControl(TabbedPanel):
    pass

class HistoryPanelItem(TabbedPanelItem):
    pass


class Historyme(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.Labid=""
        self.Labcustname=""
        self.Labattname=""
        conn = sqlite3.connect('primebank.db')
        a = conn.cursor()
        a.execute("""SELECT rowid,fname,lname FROM attendants """)
        attlist = a.fetchall()

        conn = sqlite3.connect('primebank.db')
        c= conn.cursor()
        c.execute("""SELECT rowid,fname,lname FROM customers """)
        custlist = c.fetchall()

        conn = sqlite3.connect('primebank.db')
        b= conn.cursor()
        b.execute("""SELECT rowid,* FROM transactions """)
        histlist = b.fetchall()
        conn.commit()
        conn.close()
        self.he=len(histlist)*40
        for onet in histlist:
            tranid=onet[0]
            trantype=onet[1]
            self.Labid = Label(text=str(tranid), size_hint_x=.1,height=dp(50))
            trancust=onet[2]
            for onecust in custlist:
                if trancust==onecust[0]:
                    self.Labcustname=Label(text=onecust[1]+"  "+onecust[2],size_hint_x=.3,height=dp(50))
            tranatt=onet[3]
            for oneatt in attlist:
                if tranatt==oneatt[0]:
                    self.Labattname=Label(text=oneatt[1]+"  "+oneatt[2],size_hint_x=.3,height=dp(50))
            Labtype=Label(text=trantype,size_hint_x=.3,height=dp(50))
            self.add_widget(self.Labid)
            self.add_widget(self.Labcustname)
            self.add_widget(self.Labattname)
            self.add_widget(Labtype)










class Vontrol(TabbedPanelItem):
    pass

class Welcome(Screen):
    pass

class AdminLogin(Screen):
    pass

class RegisterAttendant(Screen):
    pass

class RegisterAttendantSuccess(Screen):
    pass

class AttendantsDashboard(Screen):
    pass

class AttendantsLogin(Screen):
    pass



class WelcomeMainLayout(BoxLayout):
    pass

class Box1(BoxLayout):
    pass

class Box2(BoxLayout):
    pass

class Box3(BoxLayout):
    pass
class Box4(BoxLayout):
    pass

class Box5(BoxLayout):
    pass

class Box6(BoxLayout):
    pass

class Box7(BoxLayout):
    pass
class Page2(BoxLayout):
    pass

class Screen1(Screen):
    pass

class Scrollist(ScrollView):
    pass

class Screen2(Screen):
    pass

class Screen3(Screen):
    pass

class Screen4(Screen):
    pass

class WelcomePages(PageLayout):
    pass
class AdminDash(Screen):
    pass


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title="Prime Bank Safe Deposit"
        self.icon=""


    def on_start(self):
        conn = sqlite3.connect('primebank.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS attendants( 
                                   fname text,
                                   mname text,
                                   lname text,
                                   gen text,
                                   yob integer,
                                   id text,
                                   passw text
                                   )""")
        c.execute("""CREATE TABLE IF NOT EXISTS customers( 
                                           fname text,
                                           mname text,
                                           lname text,
                                           gen text,
                                           yob integer,
                                           id text,
                                           custphoto blob,
                                           phone text,
                                           email text,
                                           secret text,
                                           registered_by integer
                                           )""")
        c.execute("""CREATE TABLE IF NOT EXISTS transactions(
                                                   transaction_type text,
                                                   customer integer,
                                                   attendant integer
                                                   )""")
        conn.commit()
        conn.close()
    def exitapp(self):
        self.stop()


MainApp().run()
