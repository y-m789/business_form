import os
import math
from datetime import datetime
from flask import *
from flask import render_template
from app.database import mk_db
from app.database import Content
from app.database import BaseInfo
from app.write_template import WriteTemplate


app = Flask(__name__)
db = mk_db()
XLSX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
NUM_ITEM = 8  # 入力できる品目の数


@app.route("/", methods=["GET", "POST"])
def root():
    """
    メインページの処理
    :return:
        mainpage.htmlを表示
    """
    cont = db.query(Content).all()
    if request.method == "GET":
        return render_template("mainpage.html", cont=cont)


@app.route("/input_base", methods=["GET", "POST"])
def input_base():
    """
    基本情報の入力処理処理
    基本情報は1つのみを想定
    データベースに基本情報が入力されていなければ新規登録し、
    登録済みの場合、データベースを修正する
    :return:
        input_base.htmlを表示
    """
    base = db.query(BaseInfo).get(1)
    if request.method == "GET":
        return render_template("input_base.html", base=base)

    elif request.method == "POST":
        if request.form.get("registry"):
            if base is None:
                mess = BaseInfo(name=request.form.get("name"),
                                company=request.form.get("company"),
                                department=request.form.get("department"),
                                post=request.form.get("post"),
                                address=request.form.get("address"),
                                tel=request.form.get("tel"),
                                email=request.form.get("email"),
                                bank=request.form.get("bank"),
                                memo_estimate=request.form.get("memo_estimate"),
                                memo_bill=request.form.get("memo_bill"),
                                memo_deliver=request.form.get("memo_deliver"),
                                )
                db.add(mess)
                db.commit()
                base = db.query(BaseInfo).get(1)
            else:
                base.name = request.form.get("name")
                base.company = request.form.get("company")
                base.post = request.form.get("post")
                base.address = request.form.get("address")
                base.tel = request.form.get("tel")
                base.email = request.form.get("email")
                base.bank = request.form.get("bank")
                base.memo_estimate = request.form.get("memo_estimate")
                base.memo_bill = request.form.get("memo_bill")
                base.memo_deliver = request.form.get("memo_deliver")
                db.commit()
            return render_template("input_base.html", base=base)


@app.route("/input_customer", methods=["GET", "POST"])
def input_customer():
    """
    取引先情報の入力処理
    入力された情報をデータベースに追加していく

    :return:
        mainpage.htmlを表示
    """
    cont = db.query(Content).all()
    if request.method == "GET":
        return render_template("input_customer.html", cont=cont, num_item=NUM_ITEM)
    elif request.method == "POST":
        if request.form.get("registry"):
            timestamp = datetime.now()
            mess = Content(customer=request.form.get("customer"),
                           customer_department=request.form.get("customer_department"),
                           customer_name=request.form.get("customer_name"),
                           title=request.form.get("title"),
                           item1=request.form.get("item1"),
                           volume1=request.form.get("volume1"),
                           unit1=request.form.get("unit1"),
                           price1=request.form.get("price1"),
                           tax1=request.form.get("tax1"),
                           item2=request.form.get("item2"),
                           volume2=request.form.get("volume2"),
                           unit2=request.form.get("unit2"),
                           price2=request.form.get("price2"),
                           tax2=request.form.get("tax2"),
                           item3=request.form.get("item3"),
                           volume3=request.form.get("volume3"),
                           unit3=request.form.get("unit3"),
                           price3=request.form.get("price3"),
                           tax3=request.form.get("tax3"),
                           item4=request.form.get("item4"),
                           volume4=request.form.get("volume4"),
                           unit4=request.form.get("unit4"),
                           price4=request.form.get("price4"),
                           tax4=request.form.get("tax4"),
                           item5=request.form.get("item5"),
                           volume5=request.form.get("volume5"),
                           unit5=request.form.get("unit5"),
                           price5=request.form.get("price5"),
                           tax5=request.form.get("tax5"),
                           item6=request.form.get("item6"),
                           volume6=request.form.get("volume6"),
                           unit6=request.form.get("unit6"),
                           price6=request.form.get("price6"),
                           tax6=request.form.get("tax6"),
                           item7=request.form.get("item7"),
                           volume7=request.form.get("volume7"),
                           unit7=request.form.get("unit7"),
                           price7=request.form.get("price7"),
                           tax7=request.form.get("tax7"),
                           item8=request.form.get("item8"),
                           volume8=request.form.get("volume8"),
                           unit8=request.form.get("unit8"),
                           price8=request.form.get("price8"),
                           tax8=request.form.get("tax8"),
                           timestamp=timestamp
                           )
            db.add(mess)
            db.commit()
            cont = db.query(Content).all()
            return render_template("mainpage.html", cont=cont)


@app.route("/disp_customer", methods=["POST"])
def disp_customer():
    """
    取引先情報の詳細表示処理
    選択した取引先情報の表示

    :return:
        disp_customer.htmlを表示
    """
    index = int(request.form.get("detail"))
    cont = db.query(Content).get(index)

    if request.method == "POST":
        if request.form.get("detail"):
            subtotal, tax = 0, 0
            for i in range(NUM_ITEM):
                volume_name = 'volume'+str(i+1)
                price_name = 'price'+str(i+1)
                tax_name = 'tax'+str(i+1)
                if not cont.__dict__[volume_name] == '' and not cont.__dict__[price_name] == '':
                    subtotal += int(cont.__dict__[volume_name]) * int(cont.__dict__[price_name])
                    tax += math.floor(int(cont.__dict__[volume_name]) * int(cont.__dict__[price_name]) * (float(cont.__dict__[tax_name]) / 100))
            total = subtotal + tax
            return render_template("disp_customer.html",
                                   cont=cont, num_item=NUM_ITEM,
                                   subtotal=subtotal, tax=tax, total=total)


@app.route("/edit_customer", methods=["POST"])
def edit_customer():
    """
    取引先情報の修正処理
    選択した取引先情報の修正

    :return:
        edit_customer.htmlを表示
    """
    if request.method == "POST":
        if request.form.get("edit"):
            index = int(request.form.get("edit"))
            cont = db.query(Content).get(index)
            return render_template("edit_customer.html", cont=cont, num_item=NUM_ITEM)

        elif request.form.get("edit_registry"):
            index = int(request.form.get("edit_registry"))
            cont = db.query(Content).get(index)
            cont.customer = request.form.get("customer")
            cont.customer_department = request.form.get("customer_department")
            cont.customer_name = request.form.get("customer_name")
            cont.title = request.form.get("title")
            cont.item1 = request.form.get("item1")
            cont.volume1 = request.form.get("volume1")
            cont.unit1 = request.form.get("unit1")
            cont.price1 = request.form.get("price1")
            cont.tax1 = request.form.get("tax1")
            cont.item2 = request.form.get("item2")
            cont.volume2 = request.form.get("volume2")
            cont.unit2 = request.form.get("unit2")
            cont.price2 = request.form.get("price2")
            cont.tax2 = request.form.get("tax2")
            cont.item3 = request.form.get("item3")
            cont.volume3 = request.form.get("volume3")
            cont.unit3 = request.form.get("unit3")
            cont.price3 = request.form.get("price3")
            cont.tax3 = request.form.get("tax3")
            cont.item4 = request.form.get("item4")
            cont.volume4 = request.form.get("volume4")
            cont.unit4 = request.form.get("unit4")
            cont.price4 = request.form.get("price4")
            cont.tax4 = request.form.get("tax4")
            cont.item5 = request.form.get("item5")
            cont.volume5 = request.form.get("volume5")
            cont.unit5 = request.form.get("unit5")
            cont.price5 = request.form.get("price5")
            cont.tax5 = request.form.get("tax5")
            cont.item6 = request.form.get("item6")
            cont.volume6 = request.form.get("volume6")
            cont.unit6 = request.form.get("unit6")
            cont.price6 = request.form.get("price6")
            cont.tax6 = request.form.get("tax6")
            cont.item7 = request.form.get("item7")
            cont.volume7 = request.form.get("volume7")
            cont.unit7 = request.form.get("unit7")
            cont.price7 = request.form.get("price7")
            cont.tax7 = request.form.get("tax7")
            cont.item8 = request.form.get("item8")
            cont.volume8 = request.form.get("volume8")
            cont.unit8 = request.form.get("unit8")
            cont.price8 = request.form.get("price8")
            cont.tax8 = request.form.get("tax8")
            cont.timestamp = datetime.now()
            db.commit()
            return render_template("disp_customer.html", cont=cont, num_item=NUM_ITEM)


@app.route("/create", methods=["POST"])
def create():
    """
    見積書・請求書・納品書番号の入力処理
    選択したボタンによって処理を変える

    :return:
        create.htmlを表示
    """
    if request.method == "POST":
        # 見積書
        if request.form.get("estimate"):
            index = int(request.form.get("estimate"))
            cont = db.query(Content).get(index)
            return render_template("create.html", cont=cont, title='見積書')

        # 請求書
        elif request.form.get("bill"):
            index = int(request.form.get("bill"))
            cont = db.query(Content).get(index)
            return render_template("create.html", cont=cont, title='請求書')

        # 納品書
        elif request.form.get("deliver"):
            index = int(request.form.get("deliver"))
            cont = db.query(Content).get(index)
            return render_template("create.html", cont=cont, title='納品書')


@app.route("/publish", methods=["POST"])
def publish():
    """
    見積書・請求書・納品書の発行の入力処理
    入力情報をもとに各書類を作成し出力

    :return:
        csv、pdf出力
    """
    base = db.query(BaseInfo).get(1)
    if request.method == "POST":
        number = request.form.get("num")
        timestamp = datetime.strptime(request.form.get("timestamp"), '%Y-%m-%d')
        response = make_response()
        wt = WriteTemplate(NUM_ITEM)

        # publish***の名前を取得
        pub_name = []
        for n in request.form:
            if "publish" in n:
                pub_name = n

        if request.form.get(pub_name):
            index = int(request.form.get(pub_name))
            detail_cont = db.query(Content).get(index)

            # 見積書
            pub_type = []
            if "estimate" in pub_name:
                detail_cont.num_estimate = number
                detail_cont.timestamp_estimate = timestamp
                db.commit()
                wt.estimate(base, detail_cont)
                pub_type = "estimate_"
            # 請求書
            elif "bill" in pub_name:
                limit = datetime.strptime(request.form.get("limit"), '%Y-%m-%d')
                detail_cont.num_bill = number
                detail_cont.timestamp_bill = timestamp
                detail_cont.limit_bill = limit
                db.commit()
                wt.bill(base, detail_cont)
                pub_type = "bill_"
            # 納品書
            elif "deliver" in pub_name:
                detail_cont.num_deliver = number
                detail_cont.timestamp_deliver = timestamp
                db.commit()
                wt.delivery(base, detail_cont)
                pub_type = "deliver_"

            # CSV出力
            if "csv" in pub_name:
                download = pub_type+str(number)+'.xlsx'
                response.data = open('./tmp.xlsx', "rb").read()
                response.headers['Content-Disposition'] = 'attachment; filename=' + download
                response.mimetype = XLSX_MIMETYPE
                os.remove('./tmp.xlsx')
            # PDF出力
            elif "pdf" in pub_name:
                download = pub_type+str(number)+'.pdf'
                response.data = open('./tmp.xlsx', "rb").read()
                os.system("libreoffice --headless --nologo --nofirststartwizard --convert-to pdf ./tmp.xlsx --outdir ./")
                response.data = open('./tmp.pdf', "rb").read()
                response.headers['Content-Disposition'] = 'attachment; filename=' + download
                os.remove('./tmp.xlsx')
                os.remove('./tmp.pdf')
        return response


if __name__ == "__main__":
    app.run(debug=True)
