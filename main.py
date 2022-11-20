from Interface import Interface
from Wezel import Wezel
from flask import Flask, render_template
app = Flask(__name__,template_folder='templates', static_folder='static')
global interface

@app.route("/", methods=["POST","GET"])
def main():
   return render_template('index.html', dxinterface = interface)
def TEST1(interfac):
   interfac.listaWezlow.append(Wezel(1,3.00,[2,3]))
   interfac.listaWezlow.append(Wezel(2,3.00,[1,3]))
   interfac.listaWezlow.append(Wezel(3,3.00,[2,1]))

if __name__ == '__main__':
   interface=Interface()
   TEST1(interface)
   app.run(debug = True)