<script>
    import paymentMethods from '$lib/images/Mastercard_Visa.png'
    import shippingInformation from '$lib/images/DHL_Logo.png'
</script>

<div id="content" class="bg-gray-100 p-4 pt-5 text-gray-400 mt-5">
    <div class="grid grid-cols-1 gap-4 mb-4 px-6 lg:grid-cols-4 sm:grid-cols-2">
        <div class="">
            <p class="text-xl font-bold text-gray-600">Customer support:</p>
            <div class="flex flex-col">
                <p class="pt-2">E-Mail:</p>
                <p>shopcore.info@gmail.com</p>
            </div>
        </div>
        <div class="">
            <p class="text-xl font-bold text-gray-600">Payment methods:</p>
            <img src={paymentMethods} alt="Payment methods" class="w-32 ml-2 mt-2"/>
        </div>
        <div class="">
            <p class="text-xl font-bold text-gray-600">Shipping:</p>
            <img src={shippingInformation} alt="Shipping partner DHL" class="w-32 ml-2 mt-2"/>
        </div>
        <div class="">
            <p class="text-xl font-bold text-gray-600">Shop-App:</p>
            <div class="flex flex-col">
                <a href="/impressum" class="pt-2 hover:underline">Impressum</a>
                <a href="/legalInformation#terms" class="pt-1 hover:underline">General Terms and Conditions</a>
                <a href="/legalInformation#privacy" class="pt-1 hover:underline">Privacy Policy</a>
                <a href="/legalInformation#cancellation" class="pt-1 hover:underline">Cancellation Policy</a>
                <a href="/aboutUs" class="pt-1 hover:underline">About us</a>
            </div>
        </div>
    </div>
    <div class="text-center text-m">
        <p>All brand names, trademarks and product images are the property of their rightful owners and are used here for descriptive purposes only.</p>
        <p>* All prices quoted here include 19% VAT and exclude shipping costs of at least € 9.90*. All costs quoted here include 19% VAT.</p>
    </div>
    <div class="text-center mt-3">
        © 2024, Shop-App
    </div>
</div>