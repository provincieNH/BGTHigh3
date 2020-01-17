from conversion.conversionBGT import convertBGT

# main function and will call the conversion process.
def main():
    bgt_zip_path = r'D:\BGTHigh3\conversie\resources'

    convertBGT(bgt_zip_path)


# run python main.py will start the conversion
if __name__ == '__main__':
    try:
        main()
    except:
        raise Exception("Failed with Exception")
