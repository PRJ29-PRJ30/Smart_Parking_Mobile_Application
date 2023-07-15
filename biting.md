**MOBILE APPLICATION**

Phones have essentially become the focal point of our everyday lives, and the mobile applications we utilize have begun to offer significant conveniences in various domains. Taking these conveniences into consideration, it was determined that employing a mobile application would be an ideal approach to ensure users' expedient accessibility in the project at hand. Within our project, a mobile application has been developed for users to make reservations prior to reaching the designated parking area. To enhance usability within the mobile application, a singular screen and a user-friendly interface have been implemented.

**1- Design Phases in Mobile Application Development**

1. ` `Prior to making the decision to develop a mobile application, research was conducted to determine the programming language that could be used within this short timeframe. Among several alternatives, Python programming language was chosen as the most suitable option. Factors such as the proficiency of team members in Python programming language, easy access to Firebase, which would be used for the database, and the availability of up-to-date and extensive Firebase-related libraries influenced our decision.
1. ` `In the research conducted for the mobile application to be developed using Python programming language, Kivy and KivyMD libraries were preferred due to their extensive resources and ease of coding structure.

*Figure 1**
1. ![](Aspose.Words.0c7a9485-84aa-498e-bef4-a6caa28eba1c.001.png)![metin, bilgisayar, ekran görüntüsü, web sitesi içeren bir resim

Açıklama otomatik olarak oluşturuldu](Aspose.Words.0c7a9485-84aa-498e-bef4-a6caa28eba1c.002.jpeg) The determination of the information that users need to input was based on the decisions regarding the license plate recognition system and the data required for barrier movements. In accordance with these decisions, the data that users need to enter through the mobile application are as follows: (Figure 1)
- License Plate
- Date
- Check-in Time
- Check-out Time
- Parking Slot
- Your Slot (Reserved Slot)
- Time



**2- Usage Cases of the Application**

Case 1: Reservation

If the user wants to make a new reservation, the following steps are applied.

- Step 1: Install the mobile application on your phone.
- Step 2: Open the application when you want to make a reservation.
- Step 3: Fill in the License Plate, Date, Check-in, Check-out, and Parking Slot information in the application. (Figure 1)
- Step 4: Click the Reserved button.
- Step 5: Click the PAY button on the popup screen to make the payment for the reservation fee displayed. (Figure 2)
- Step 6: Enter your credit card information on the payment screen and make the payment. (Figure 3)
- Step 7: Click the Complete button.

The first reservation is successfully completed by following these steps, and these data are seen in the Firebase Database.

*Figure 3*

*Figure 2*
![](Aspose.Words.0c7a9485-84aa-498e-bef4-a6caa28eba1c.003.png)![metin, ekran görüntüsü, tasarım içeren bir resim

Açıklama otomatik olarak oluşturuldu](Aspose.Words.0c7a9485-84aa-498e-bef4-a6caa28eba1c.004.jpeg)![](Aspose.Words.0c7a9485-84aa-498e-bef4-a6caa28eba1c.005.png)![metin, ekran görüntüsü içeren bir resim

Açıklama otomatik olarak oluşturuldu](Aspose.Words.0c7a9485-84aa-498e-bef4-a6caa28eba1c.006.png)
















Case 2: Delayed Arrival

If the user arrives after the check-out time indicated in their reservation details, the following steps are applied.

- Step 1: Open the mobile application.
- Step 2: Enter Your Slot and Time information in the white area of the application interface. (Figure 1)

(Your Slot: The name of the slot where your vehicle is located in the reservation system)

(Time: The time you arrived to remove your vehicle)

- Step 3: Click GO OUT!! button,
- Step 4: On the popup screen, you will see the fee you need to pay for the delay and the steps you need to take. (Figure 4)
- Step 5: Click the Pay button and enter your credit card information on the payment screen to complete the payment.
- Step 6: Click the Bar-down button and remove your vehicle from the parking area after the barrier is lowered.
- Step 7: Make sure you have removed your vehicle and click the Bar-up button.
- Step 8: Click the Cancel button.

![metin, ekran görüntüsü, yazılım, multimedya içeren bir resim

Açıklama otomatik olarak oluşturuldu](Aspose.Words.0c7a9485-84aa-498e-bef4-a6caa28eba1c.007.jpeg)

*Figure 4*

Case 3: Early Arrival

If the user arrives before the check-in time indicated in their reservation details, the following steps are applied.

- Step 1: Open the mobile application.
- Step 2: Enter Your Slot and Time information in the white area of the application interface. (Figue 1)

(Your Slot: The name of the slot where your vehicle is located in the reservation system)

(Time: The time you arrived to remove your vehicle or the check-in time in the reservation)

- Step 3: Click GO OUT!! button,
- Step 4: On the popup screen, you will see that you do not need to pay any fee and the steps you need to take. (Figure 5)
- Step 5: Remove your vehicle from the parking area.
- Step 6: Make sure you have removed your vehicle and click the Bar-up button.
- Step 7: Click the Cancel button.

![metin, ekran görüntüsü, yazılım, web sayfası içeren bir resim

Açıklama otomatik olarak oluşturuldu](Aspose.Words.0c7a9485-84aa-498e-bef4-a6caa28eba1c.008.jpeg)

*Figure 5*
