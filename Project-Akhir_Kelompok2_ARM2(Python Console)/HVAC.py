import mysql.connector
import random, datetime, time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tukangsapu0721",
  database="db_tugasakhir"
)
mycursor = mydb.cursor()

def Menu():
    print("SIMULATOR MESIN")
    print("1. Show Data Monitoring HVAC")
    print("2. Delete Data User di Monitoring HVAC")
    print("---------------------")
    print("3. Exit Program")
    print()
    choice = int(input("Enter here: "))

    if(choice==1):
        for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(1.5)
            temp1_cn = random.randint(55,65)
            temp2_cn = temp1_cn - 10
            temp1_ev = random.randint(55,65)
            temp2_ev = temp1_ev + 15
            comp = random.randint (50,90)
            room = random.randint (27,35)
            
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO tb_hvac (tanggal, in_condensor, out_condensor, in_evaporator, out_evaporator, compressor, room) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                             (date_time, temp1_cn, temp2_cn, temp1_ev, temp2_ev, comp, room))
            mydb.commit()
            print(mycursor.rowcount, "Membaca Kondisi HVAC")     

    if(choice==2):
            mycursor = mydb.cursor()
            mycursor.execute("DELETE FROM tb_user where id = 1")
            mydb.commit()
            print(mycursor.rowcount, "Menghapus Data")
        
    if(choice==3):
        exit()
        
    lagi=input("\nUlangi ga (Y/y) ? ")
    if lagi.lower() == "y" :
        Menu ()
    else :
        print("Program selesai")

Menu()