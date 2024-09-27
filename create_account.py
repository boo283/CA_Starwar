from utils import *
import pandas as pd



if __name__ == '__main__':

    data = pd.read_excel("data.xlsx")
    #data = data[data['created'] == 0]
    data['sdt']=data['sdt'].apply(add_0_sdt)
    cnt = 0

    for row in reversed(list(data.iterrows())):
        if data.loc[row[0], 'created'] == 1 or data.loc[row[0], 'created'] == '1':
            continue
        if data.loc[row[0], 'login_test'] == -1 or data.loc[row[0], 'login_test'] == '-1':
            continue
        try:
            driver=configure_driver()

            register_url = 'https://starawards.vn/register#form'
            driver.get(register_url)
            zoom_out_browser()
            personal_data = row[1]

            if create_account(driver, personal_data):
                #change created status to 1
                #data.loc[row[0], 'created'] = 1
                print('Successfully')
                with open('su_success.txt', 'a') as f:
                    f.write(f"{data.loc[row[0], 'masv']}\n")
            else:
                print("Failed")
                time.sleep(3)
                data.loc[row[0], 'created'] = 1
                with open('su_failed.txt', 'a') as f:
                    f.write(f"{data.loc[row[0], 'masv']}\n")

            # write log

            driver.delete_all_cookies()
            #driver.refresh()
            
            sleep(2)
        except KeyboardInterrupt:
            break
        except:
            continue
    data.to_excel("new_data.xlsx", index=False)       

