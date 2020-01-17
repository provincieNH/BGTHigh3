from conversion.conversionBGT import convertBGT

# main function and will call the conversion process.
def main():
    input_path = r'D:\BGTHigh3\conversie\resources'
    output_path = r'D:\BGTHigh3\conversie\output'

    convertBGT(input_path, output_path)


# run python main.py will start the conversion
if __name__ == '__main__':
    try:
        main()
    except:
        raise Exception("Failed with Exception")
