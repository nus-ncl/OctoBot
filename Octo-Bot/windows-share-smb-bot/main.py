from smb.SMBConnection import SMBConnection
import time

def getSharedFolder(userID, password, client_machine_name, server_name, domain_name):

    conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                     is_direct_tcp=True)
    conn.connect(server_ip, 445)

    shares = conn.listShares()

    for share in shares:
      if not share.isSpecial and share.name not in ['NETLOGON', 'SYSVOL']:
          sharedfiles = conn.listPath(share.name, '/')
          for sharedfile in sharedfiles:
              print(sharedfile.filename)
              if sharedfile.filename == "File-in-windows.txt":
                  fileObj = open('File-in-windows.txt','wb') 
                  conn.retrieveFile(share.name,sharedfile.filename,fileObj)
                  fileObj.close() 
                  print(sharedfile.filename+" is downloaded in the current local directory")
                  fileObj2 = open('File-in-linux.txt','rb')
                  file = 'File-in-linux.txt' 
                  conn.storeFile(share.name,'/'+file,fileObj2)
                  print(file+" is uploaded in remote shared directory") 
    conn.close()

if __name__ == "__main__":

  userID = 'workshop'
  password = 'MySOC'
  client_machine_name = 'ubuntu-18'
  server_name = 'ncl012'
  server_ip = '172.26.191.217'
  domain_name = 'NCL012'

  while True:
     getSharedFolder(userID, password, client_machine_name, server_name, domain_name)
     time.sleep(5)

