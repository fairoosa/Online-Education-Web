def create_cert(name, filename):
    print("filename", filename)
    import cv2
    try:
        # certificate_template_image = cv2.imread(r"C:\Users\fairo\mini\Mini-Project-main\Mini-Project-main\Mini-Project-main\edtech\user_management\certificate-template.jpg")
        certificate_template_image = cv2.imread(r"C:\Users\fairo\OneDrive\Documents\work\Mini-Project-main\edtech\user_management\certificate-template.jpg")
    except Exception as e:
        print("exceprrr", e)
    print("imagee: ", certificate_template_image)
    cv2.putText(certificate_template_image, name.strip(), (815,1500), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 250), 5, cv2.LINE_AA)
    cv2.imwrite(f"{filename}", certificate_template_image)



