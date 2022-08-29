import pandas as pd

def password_keystroke(file_path, file_dest):
  df = pd.read_csv(file_path)
  df['totalT'] = df['DD.period.t'] + df['DD.t.i'] + df['DD.i.e'] + df['DD.e.five'] + df['DD.five.Shift.r'] + df['DD.o.a'] + df['DD.a.n'] + df['DD.n.l'] + df['DD.l.Return']
  df['averageT'] = df['totalT']/9.0
  df.to_csv(file_dest)

def keyboard_activity(file_path, file_dest):
  df2 = pd.read_csv(file_path)
  df2['dt_end'] = df2['dt_start'].shift(-1)
  df2['interval'] = df2['dt_end'] - df2['dt_start']
  is_below_limit = df2['interval'] < 1000
  df2 = df2[is_below_limit].groupby('session_id').apply(lambda x: x.head(-1))
  df2.to_csv(file_dest)

print("*****     Starting Preprocessing     ******")

password_keystroke('password-speed/DSL-StrongPasswordData.csv', 'DSL-StrongPasswordData-processed.csv')
keyboard_activity('browser-activity/activity_keyboard.csv', 'activity_keyboard_processed.csv')

print("*****     End Preprocessing     ******")