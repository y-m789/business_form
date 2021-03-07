from app.app import app


def main():
    # 外部公開する場合はhost, portを変更する
    app.run(debug=False, host='127.0.0.1', port=8008)


if __name__ == "__main__":
    main()
