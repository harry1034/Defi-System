import os
from flask import Flask, jsonify, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField
from brownie import accounts, Contract , network
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = "C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb"
network.connect('goerli')
usdcAddress = Contract('0x96Eaf2cc9fD7f4693d8287F6531234ddd220fEef')
defi_contract = Contract('0xBA237c88271e30989784528db033b157996e3FdF')

account = accounts.add(os.getenv("PRIVATE_KEY"))
accounts.add(os.getenv("PRIVATE_KEY1"))
accounts.add(os.getenv("PRIVATE_KEY2"))

class Form(FlaskForm):
    Faccounts = SelectField('Account' , choices = ['0xfFF0D3D68D80Fd30b158dcc4eCa1217DAC20f785',
                                                    '0x9Cf267F9B90B072db0a27a23c190e7E40F961842',
                                                    '0xF3cbcD528bb67C0EE3fCBE8e160828bF6fdbf92a'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deposit')
def deposit():
    form = Form()
    AvailableBal = SC_getAccountbal() / 10 ** 18
    DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
    return render_template('deposit.html', form = form, AvailableBal = AvailableBal, DepositedAmount = DepositedAmount)

@app.route('/depositButton', methods =['GET', 'POST'])
def depositButton():
    form = Form()
    if request.method == 'POST':
        depositAmount = request.form.get("depositValue", type = int) * (10 ** 18)
        SC_depositBal(depositAmount)
        DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
        AvailableBal = usdcAddress.balanceOf(account) /(10 ** 18)
    return render_template('deposit.html',form = form,  AvailableBal = AvailableBal, DepositedAmount = DepositedAmount)

@app.route('/withdrawButton', methods =['GET', 'POST'])
def withdrawButton():
    form = Form()
    if request.method == 'POST':
        withdrawAmount = request.form.get("withdrawValue", type = int) * (10 ** 18)
        SC_withdrawBal(withdrawAmount)
        DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
        AvailableBal = usdcAddress.balanceOf(account) /(10 ** 18)
    return render_template('deposit.html',form = form,  AvailableBal = AvailableBal, DepositedAmount = DepositedAmount)

def SC_withdrawBal(withdrawAmount):
    defi_contract.withdraw(withdrawAmount, {"from": account})

def SC_getAccountbal():
    balance = usdcAddress.balanceOf(account)
    return balance

def SC_depositBal(depositAmount):
    usdcAddress.approve(defi_contract, depositAmount, {"from": account})
    defi_contract.depositToken(depositAmount, {"from": account})

@app.route('/refresh/<currentAccount>')
def refresh(currentAccount):
    global account
    account = accounts.at(currentAccount)
    currentBal = usdcAddress.balanceOf(account) /(10 ** 18)
    stakedBalance = defi_contract.depositBalance(account) / (10 ** 18)
    return jsonify({'response' : currentAccount ,'stakedBalance' : stakedBalance , 'currentBal': currentBal})

@app.route('/FundMe', methods =["GET", "POST"])
def FundMe():
    if request.method == "POST":
        FromAddress = request.form.get("fromAddress")
        FromAddress = accounts.at(FromAddress, force=True)
        ToAddress = request.form.get("toAddress")
        Amount = request.form.get("Amount", type = int)
        usdcAddress.transfer(ToAddress, Amount * 10 ** 18, {"from": FromAddress})
    return render_template('FundMe.html')

if __name__ == "__main__":
    
    app.run()
    network.disconnect()