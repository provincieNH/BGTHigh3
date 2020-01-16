from conversion.conversionBGT import convertBGT

# main function and will call the conversion process.
def main():
    convertBGT()


# run python main.py will start the conversion
if __name__ == '__main__':
    try:
        main()
    except:
        raise Exception("Failed with Exception")
