import flet as ft
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# CONNECT DATABASE
engine = create_engine("sqlite:///db/dbperson.db")

# MAPPING THE TABLE
Base = declarative_base()
class User(Base):
	# YOU TABLE NAME HERE
	__tablename__="users"
	id = Column(Integer,primary_key=True)
	name = Column(String)
	age = Column(Integer)


class Myclass(ft.UserControl):
	def __init__(self):
		super().__init__()
		self.alldata = ft.Column()
		self.addBtn = ft.ElevatedButton("add new data",
			on_click=self.addnewData
			)
		self.editBtn = ft.ElevatedButton("Edit",
			bgcolor="orange",color="white",
			on_click=self.saveEdit
			)
		# VISIBLE FOR HIDE AND SHOW BUTTON
		self.addBtn.visible = True
		self.editBtn.visible = False
		self.selectId = ft.Text("",size=30)
		self.selectId.visible = False



	def build(self):
		self.nameInput = ft.TextField(label="USername")
		self.ageInput = ft.TextField(label="Age ")

		return ft.Column([
			self.selectId,
			self.nameInput,
			self.ageInput,
			self.addBtn,
			self.editBtn,
			self.alldata

			])
		
	# ADD NEW DATA TO TABLE
	def addnewData(self,e):
		new_user = User(name=self.nameInput.value,age=self.ageInput.value)
		Session = sessionmaker(bind=engine)
		session = Session()
		session.add(new_user)
		# COMMIT
		session.commit()

		# REFRESH THE DATA
		self.alldata.controls.clear()
		# CALL RENDER FUNCTION
		self.CallFromDatabase()
		self.page.update()



	# LIFECYCLE FOR CALL FUNCTION BEFORE WIDGET RENDER
	def did_mount(self):
		self.CallFromDatabase()


	def CallFromDatabase(self):
		new_user = User()
		Session = sessionmaker(bind=engine)
		session = Session()
		# COMMIT
		session.commit()
		# FETCH ALL DATA FROM TABLE
		users = session.query(User).all()
		for u in users:
			self.alldata.controls.append(
			ft.Container(
				bgcolor="red",
				padding=10,
			content=ft.Column([
			ft.Text(f"name : {u.name}",
			color="white",
			size=25
			),
			ft.Text(f"name : {u.age}",
			color="white",
			size=20
			),
			# EDIT AND DELETE BUTTON HERE 
			ft.Row([
			ft.ElevatedButton("Edit",
			data=u,
			on_click=lambda e:self.prosesEdit(e)
				),

			ft.ElevatedButton("Delete",
			data=u,
			on_click=lambda e:self.prosesDelete(e)
				),

				])


				])

				)

			)
		# UPDATE ALL
		self.update()

	# DELETE BUTTON ACTION LOGIC HERE
	def prosesDelete(self,e):
		# GET ID FROM LOOP ABOVE
		self.selectId.value = e.control.data.id
		the_id = self.selectId.value
		Session = sessionmaker(bind=engine)
		session = Session()
		user_to_delete = session.query(User).filter(User.id == int(the_id)).first()
		# DELETE ACTION
		session.delete(user_to_delete)
		session.commit()
		# REFRESH DATA AFTER ADD NEW DATA TO TABLE
		# REFRESH THE DATA
		self.alldata.controls.clear()
		# CALL RENDER FUNCTION
		self.CallFromDatabase()
		self.page.update()

	# EDIT BUTTON
	def prosesEdit(self,e):
		# HIDE ADD NEW BUTTON 
		self.addBtn.visible = False
		self.selectId.visible =True
		# GET DATA ID 
		self.selectId.value = e.control.data.id

		# SET INPUT FOR GET YOU CLICK DETAILS EDIT
		self.nameInput.value  =  e.control.data.name
		self.ageInput.value  =  e.control.data.age
		self.editBtn.visible = True
		self.update()

	# NOW IF prosessEdit Save Then save you edit to table

	def saveEdit(self,e):
		self.addBtn.visible = True
		Session = sessionmaker(bind=engine)
		session = Session()
		# GET DATA ID 
		the_id = self.selectId.value
		user_to_update = session.query(User).filter(User.id == the_id).first()

		# CHANGE NAME AND AGE FOR EDIT
		user_to_update.name = self.nameInput.value
		user_to_update.age = self.ageInput.value
		session.commit()

		# CLEAR INPUT TEXT AFTER EDIT
		self.nameInput.value = ""
		self.ageInput.value = ""
		self.editBtn.visible = False
		self.selectId.visible = False

		# REFRESH DATA AGAIN
		# REFRESH THE DATA
		self.alldata.controls.clear()
		# CALL RENDER FUNCTION
		self.CallFromDatabase()
		self.page.update()









def main(page):
	page.update()
	myclass = Myclass()
	page.add(myclass)

ft.app(target=main)
