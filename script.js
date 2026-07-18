const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

const whatsappFloat = document.getElementById('whatsapp-float');
if (whatsappFloat) {
  setTimeout(() => whatsappFloat.classList.add('visible'), 3000);
}

const siteHeader = document.querySelector('.site-header');
if (siteHeader) {
  const toggleHeaderBg = () => siteHeader.classList.toggle('scrolled', window.scrollY > 40);
  toggleHeaderBg();
  window.addEventListener('scroll', toggleHeaderBg);
}

const navToggle = document.getElementById('nav-toggle');
const mainNav = document.getElementById('main-nav');
if (navToggle && mainNav) {
  navToggle.addEventListener('click', () => {
    const isOpen = mainNav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });
}

document.querySelectorAll('.nav-dropdown-toggle').forEach((toggle) => {
  toggle.addEventListener('click', () => {
    if (window.innerWidth > 900) return;
    const dropdown = toggle.closest('.nav-dropdown');
    dropdown.classList.toggle('open');
  });
});

const quoteWidget = document.getElementById('quote-widget');
if (quoteWidget) {
  const PRICES = {
    "Šibenik - center": {
      "Šibenik Bus Station": 10,
      "Šibenik Ferry Port": 10,
      "D-Marin Marina Mandalina Šibenik": 15,
      "Amadria Park Hotel Šibenik": 18,
      "Brodarica - Šibenik": 25,
      "Zablaće": 18,
      "Žaborić": 25,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 50,
      "Rogoznica": 65,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 30,
      "Zaton": 25,
      "Marina Zaton": 20,
      "Srima": 25,
      "Vodice": 30,
      "Tribunj": 40,
      "Pirovac": 50,
      "Tisno": 50,
      "Jezera": 55,
      "Murter": 70,
      "Betina": 70,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 130,
      "Bilice": 20,
      "Tromilja": 40,
      "NP Krka - Lozovac entrance": 45,
      "Lozovac": 45,
      "Skradin - center": 50,
      "NP Krka - Skradin entrance": 50,
      "Marina ACI Skradin": 50,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Šibenik Bus Station": {
      "Šibenik - center": 10,
      "D-Resort Hotel Šibenik": 15,
      "Bellevue Superior Hotel Šibenik": 15,
      "D-Marin Marina Mandalina Šibenik": 15,
      "Amadria Park Hotel Šibenik": 18,
      "Brodarica - Šibenik": 25,
      "Zablaće": 18,
      "Žaborić": 25,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 50,
      "Rogoznica": 65,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 30,
      "Zaton": 25,
      "Marina Zaton": 20,
      "Srima": 25,
      "Vodice": 30,
      "Tribunj": 40,
      "Pirovac": 50,
      "Tisno": 50,
      "Jezera": 55,
      "Murter": 70,
      "Betina": 70,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 130,
      "Bilice": 20,
      "Tromilja": 40,
      "NP Krka - Lozovac entrance": 45,
      "Lozovac": 45,
      "Skradin - center": 50,
      "NP Krka - Skradin entrance": 50,
      "Marina ACI Skradin": 50,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Šibenik Ferry Port": {
      "Šibenik - center": 10,
      "D-Resort Hotel Šibenik": 15,
      "Bellevue Superior Hotel Šibenik": 15,
      "D-Marin Marina Mandalina Šibenik": 15,
      "Amadria Park Hotel Šibenik": 18,
      "Brodarica - Šibenik": 25,
      "Zablaće": 18,
      "Žaborić": 25,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 50,
      "Rogoznica": 65,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 30,
      "Zaton": 25,
      "Marina Zaton": 20,
      "Srima": 25,
      "Vodice": 30,
      "Tribunj": 40,
      "Pirovac": 50,
      "Tisno": 50,
      "Jezera": 55,
      "Murter": 70,
      "Betina": 70,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 130,
      "Bilice": 20,
      "Tromilja": 40,
      "NP Krka - Lozovac entrance": 45,
      "Lozovac": 45,
      "Skradin - center": 50,
      "NP Krka - Skradin entrance": 50,
      "Marina ACI Skradin": 50,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "D-Resort Hotel Šibenik": {
      "Šibenik - center": 15,
      "D-Marin Marina Mandalina Šibenik": 15,
      "Amadria Park Hotel Šibenik": 18,
      "Brodarica - Šibenik": 25,
      "Zablaće": 18,
      "Žaborić": 25,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 50,
      "Rogoznica": 65,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 30,
      "Zaton": 25,
      "Marina Zaton": 20,
      "Srima": 25,
      "Vodice": 30,
      "Tribunj": 40,
      "Pirovac": 50,
      "Tisno": 50,
      "Jezera": 55,
      "Murter": 70,
      "Betina": 70,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 130,
      "Bilice": 20,
      "Tromilja": 40,
      "NP Krka - Lozovac entrance": 45,
      "Lozovac": 45,
      "Skradin - center": 50,
      "NP Krka - Skradin entrance": 50,
      "Marina ACI Skradin": 50,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Bellevue Superior Hotel Šibenik": {
      "Šibenik - center": 15,
      "D-Resort Hotel Šibenik": 15,
      "D-Marin Marina Mandalina Šibenik": 15,
      "Amadria Park Hotel Šibenik": 18,
      "Brodarica - Šibenik": 25,
      "Zablaće": 18,
      "Žaborić": 25,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 50,
      "Rogoznica": 65,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 30,
      "Zaton": 25,
      "Marina Zaton": 20,
      "Srima": 25,
      "Vodice": 30,
      "Tribunj": 40,
      "Pirovac": 50,
      "Tisno": 50,
      "Jezera": 55,
      "Murter": 70,
      "Betina": 70,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 130,
      "Bilice": 20,
      "Tromilja": 40,
      "NP Krka - Lozovac entrance": 45,
      "Lozovac": 45,
      "Skradin - center": 50,
      "NP Krka - Skradin entrance": 50,
      "Marina ACI Skradin": 50,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "D-Marin Marina Mandalina Šibenik": {
      "Šibenik - center": 15,
      "Amadria Park Hotel Šibenik": 18,
      "Brodarica - Šibenik": 20,
      "Zablaće": 18,
      "Žaborić": 25,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 50,
      "Rogoznica": 65,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 40,
      "Zaton": 35,
      "Marina Zaton": 30,
      "Srima": 30,
      "Vodice": 35,
      "Tribunj": 40,
      "Pirovac": 50,
      "Tisno": 55,
      "Jezera": 60,
      "Murter": 70,
      "Betina": 70,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 130,
      "Bilice": 25,
      "Tromilja": 40,
      "NP Krka - Lozovac entrance": 45,
      "Lozovac": 45,
      "Skradin - center": 50,
      "NP Krka - Skradin entrance": 50,
      "Marina ACI Skradin": 50,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Amadria Park Hotel Šibenik": {
      "Šibenik - center": 18,
      "D-Marin Marina Mandalina Šibenik": 18,
      "Brodarica - Šibenik": 25,
      "Žaborić": 28,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 50,
      "Rogoznica": 65,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 40,
      "Zaton": 35,
      "Marina Zaton": 30,
      "Srima": 35,
      "Vodice": 40,
      "Tribunj": 45,
      "Pirovac": 55,
      "Tisno": 55,
      "Jezera": 65,
      "Murter": 80,
      "Betina": 80,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 130,
      "Bilice": 30,
      "Tromilja": 40,
      "NP Krka - Lozovac entrance": 45,
      "Lozovac": 45,
      "Skradin - center": 50,
      "NP Krka - Skradin entrance": 50,
      "Marina ACI Skradin": 50,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Amadria Park Camp": {
      "Šibenik - center": 18,
      "D-Resort Hotel Šibenik": 18,
      "Bellevue Superior Hotel Šibenik": 18,
      "D-Marin Marina Mandalina Šibenik": 18,
      "Brodarica - Šibenik": 25,
      "Žaborić": 28,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 50,
      "Rogoznica": 65,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 40,
      "Zaton": 35,
      "Marina Zaton": 30,
      "Srima": 35,
      "Vodice": 40,
      "Tribunj": 45,
      "Pirovac": 55,
      "Tisno": 55,
      "Jezera": 65,
      "Murter": 80,
      "Betina": 80,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 130,
      "Bilice": 30,
      "Tromilja": 40,
      "NP Krka - Lozovac entrance": 45,
      "Lozovac": 45,
      "Skradin - center": 50,
      "NP Krka - Skradin entrance": 50,
      "Marina ACI Skradin": 50,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Brodarica - Šibenik": {
      "Šibenik - center": 25,
      "D-Marin Marina Mandalina Šibenik": 20,
      "Amadria Park Hotel Šibenik": 25,
      "Zablaće": 25,
      "Žaborić": 25,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 45,
      "Rogoznica": 65,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 40,
      "Zaton": 40,
      "Marina Zaton": 40,
      "Srima": 35,
      "Vodice": 40,
      "Tribunj": 45,
      "Pirovac": 55,
      "Tisno": 60,
      "Jezera": 60,
      "Murter": 80,
      "Betina": 80,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 135,
      "Tromilja": 50,
      "NP Krka - Lozovac entrance": 55,
      "Lozovac": 55,
      "Skradin - center": 55,
      "NP Krka - Skradin entrance": 55,
      "Marina ACI Skradin": 55,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 80,
      "Knin": 95
    },
    "Zablaće": {
      "Šibenik - center": 18,
      "D-Marin Marina Mandalina Šibenik": 18,
      "Brodarica - Šibenik": 25,
      "Žaborić": 28,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 50,
      "Rogoznica": 65,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 40,
      "Zaton": 35,
      "Marina Zaton": 30,
      "Srima": 35,
      "Vodice": 40,
      "Tribunj": 45,
      "Pirovac": 55,
      "Tisno": 55,
      "Jezera": 65,
      "Murter": 80,
      "Betina": 80,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 130,
      "Bilice": 30,
      "NP Krka - Lozovac entrance": 45,
      "Skradin - center": 50,
      "NP Krka - Skradin entrance": 50,
      "Marina ACI Skradin": 50,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Žaborić": {
      "Šibenik - center": 25,
      "D-Marin Marina Mandalina Šibenik": 25,
      "Amadria Park Hotel Šibenik": 28,
      "Brodarica - Šibenik": 25,
      "Zablaće": 28,
      "Grebaštica": 35,
      "Bilo": 40,
      "Primošten": 45,
      "Rogoznica": 40,
      "Split Airport (SPU)": 95,
      "Trogir": 80,
      "Split": 130,
      "Dubrovnik": 460,
      "Dubrovnik Airport (DBV)": 460,
      "Jadrija": 55,
      "Zaton": 50,
      "Marina Zaton": 45,
      "Srima": 50,
      "Vodice": 50,
      "Tribunj": 60,
      "Pirovac": 70,
      "Tisno": 65,
      "Jezera": 80,
      "Murter": 95,
      "Betina": 95,
      "Zadar": 150,
      "Zadar Airport (ZAD)": 140,
      "Tromilja": 50,
      "NP Krka - Lozovac entrance": 55,
      "Lozovac": 55,
      "Skradin - center": 75,
      "NP Krka - Skradin entrance": 75,
      "Marina ACI Skradin": 75,
      "Drniš": 69,
      "NP Krka - Roški Slap entrance": 115,
      "Knin": 99
    },
    "Grebaštica": {
      "Šibenik - center": 35,
      "D-Marin Marina Mandalina Šibenik": 35,
      "Amadria Park Hotel Šibenik": 35,
      "Brodarica - Šibenik": 35,
      "Zablaće": 35,
      "Žaborić": 35,
      "Bilo": 40,
      "Primošten": 45,
      "Rogoznica": 30,
      "Split Airport (SPU)": 90,
      "Trogir": 80,
      "Split": 130,
      "Dubrovnik": 450,
      "Dubrovnik Airport (DBV)": 450,
      "Jadrija": 65,
      "Zaton": 60,
      "Marina Zaton": 55,
      "Srima": 60,
      "Vodice": 55,
      "Tribunj": 75,
      "Pirovac": 85,
      "Tisno": 70,
      "Jezera": 90,
      "Murter": 105,
      "Betina": 105,
      "Zadar": 155,
      "Zadar Airport (ZAD)": 140,
      "Tromilja": 70,
      "NP Krka - Lozovac entrance": 75,
      "Lozovac": 75,
      "Skradin - center": 80,
      "NP Krka - Skradin entrance": 80,
      "Marina ACI Skradin": 80,
      "Drniš": 69,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 99
    },
    "Bilo": {
      "Šibenik - center": 40,
      "D-Marin Marina Mandalina Šibenik": 40,
      "Amadria Park Hotel Šibenik": 40,
      "Brodarica - Šibenik": 40,
      "Zablaće": 40,
      "Žaborić": 40,
      "Grebaštica": 40,
      "Primošten": 45,
      "Rogoznica": 25,
      "Split Airport (SPU)": 80,
      "Trogir": 80,
      "Split": 130,
      "Dubrovnik": 445,
      "Dubrovnik Airport (DBV)": 445,
      "Jadrija": 70,
      "Zaton": 65,
      "Marina Zaton": 60,
      "Srima": 65,
      "Vodice": 60,
      "Tribunj": 80,
      "Pirovac": 90,
      "Tisno": 90,
      "Jezera": 95,
      "Murter": 110,
      "Betina": 110,
      "Zadar": 160,
      "Zadar Airport (ZAD)": 145,
      "Tromilja": 75,
      "NP Krka - Lozovac entrance": 80,
      "Lozovac": 80,
      "Skradin - center": 85,
      "NP Krka - Skradin entrance": 85,
      "Marina ACI Skradin": 85,
      "Drniš": 75,
      "NP Krka - Roški Slap entrance": 125,
      "Knin": 105
    },
    "Primošten": {
      "Šibenik - center": 50,
      "D-Marin Marina Mandalina Šibenik": 50,
      "Amadria Park Hotel Šibenik": 50,
      "Brodarica - Šibenik": 50,
      "Zablaće": 50,
      "Žaborić": 45,
      "Grebaštica": 45,
      "Bilo": 45,
      "Rogoznica": 15,
      "Split Airport (SPU)": 80,
      "Split": 130,
      "Dubrovnik": 450,
      "Dubrovnik Airport (DBV)": 450,
      "Jadrija": 65,
      "Zaton": 75,
      "Marina Zaton": 70,
      "Srima": 75,
      "Vodice": 70,
      "Tribunj": 90,
      "Pirovac": 100,
      "Tisno": 80,
      "Jezera": 105,
      "Murter": 120,
      "Betina": 120,
      "Zadar": 170,
      "Zadar Airport (ZAD)": 160,
      "Tromilja": 75,
      "NP Krka - Lozovac entrance": 80,
      "Lozovac": 80,
      "Skradin - center": 80,
      "NP Krka - Skradin entrance": 80,
      "Marina ACI Skradin": 85,
      "Drniš": 85,
      "NP Krka - Roški Slap entrance": 110,
      "Knin": 115
    },
    "Rogoznica": {
      "Šibenik - center": 65,
      "D-Marin Marina Mandalina Šibenik": 65,
      "Amadria Park Hotel Šibenik": 65,
      "Brodarica - Šibenik": 65,
      "Zablaće": 65,
      "Žaborić": 40,
      "Grebaštica": 30,
      "Bilo": 25,
      "Primošten": 15,
      "Split Airport (SPU)": 80,
      "Trogir": 30,
      "Split": 75,
      "Dubrovnik": 420,
      "Dubrovnik Airport (DBV)": 420,
      "Jadrija": 95,
      "Zaton": 90,
      "Marina Zaton": 85,
      "Srima": 90,
      "Vodice": 80,
      "Tribunj": 105,
      "Pirovac": 115,
      "Tisno": 115,
      "Jezera": 120,
      "Murter": 135,
      "Betina": 135,
      "Zadar": 170,
      "Zadar Airport (ZAD)": 160,
      "Tromilja": 90,
      "NP Krka - Lozovac entrance": 95,
      "Lozovac": 95,
      "Skradin - center": 90,
      "NP Krka - Skradin entrance": 90,
      "Marina ACI Skradin": 105,
      "Drniš": 90,
      "NP Krka - Roški Slap entrance": 120,
      "Knin": 120
    },
    "Split Airport (SPU)": {
      "Šibenik - center": 95,
      "D-Marin Marina Mandalina Šibenik": 95,
      "Amadria Park Hotel Šibenik": 95,
      "Brodarica - Šibenik": 95,
      "Zablaće": 95,
      "Žaborić": 95,
      "Grebaštica": 90,
      "Bilo": 80,
      "Primošten": 80,
      "Rogoznica": 80,
      "Dubrovnik": 450,
      "Dubrovnik Airport (DBV)": 450,
      "Jadrija": 115,
      "Zaton": 115,
      "Marina Zaton": 115,
      "Srima": 115,
      "Vodice": 115,
      "Tribunj": 120,
      "Pirovac": 125,
      "Tisno": 130,
      "Jezera": 135,
      "Murter": 150,
      "Betina": 150,
      "Zadar": 210,
      "Zadar Airport (ZAD)": 200,
      "Bilice": 100,
      "Tromilja": 90,
      "NP Krka - Lozovac entrance": 95,
      "Lozovac": 95,
      "Skradin - center": 110,
      "NP Krka - Skradin entrance": 110,
      "Marina ACI Skradin": 100,
      "Drniš": 80,
      "NP Krka - Roški Slap entrance": 100,
      "Knin": 110,
      "NP Plitvice Lakes": 395,
      "Zagreb": 550,
      "Zagreb Airport (ZAG)": 550
    },
    "Trogir": {
      "Šibenik - center": 95,
      "D-Marin Marina Mandalina Šibenik": 95,
      "Amadria Park Hotel Šibenik": 95,
      "Brodarica - Šibenik": 95,
      "Zablaće": 95,
      "Žaborić": 80,
      "Grebaštica": 80,
      "Bilo": 80,
      "Rogoznica": 30,
      "Dubrovnik": 420,
      "Dubrovnik Airport (DBV)": 420,
      "Jadrija": 115,
      "Zaton": 115,
      "Marina Zaton": 115,
      "Srima": 115,
      "Vodice": 110,
      "Tribunj": 120,
      "Pirovac": 125,
      "Tisno": 130,
      "Jezera": 135,
      "Murter": 150,
      "Betina": 150,
      "Zadar": 210,
      "Zadar Airport (ZAD)": 200,
      "Tromilja": 90,
      "NP Krka - Lozovac entrance": 95,
      "Lozovac": 95,
      "Skradin - center": 100,
      "NP Krka - Skradin entrance": 100,
      "Marina ACI Skradin": 94,
      "Drniš": 80,
      "NP Krka - Roški Slap entrance": 110,
      "Knin": 110
    },
    "Split": {
      "Šibenik - center": 140,
      "D-Marin Marina Mandalina Šibenik": 140,
      "Amadria Park Hotel Šibenik": 140,
      "Brodarica - Šibenik": 140,
      "Zablaće": 140,
      "Žaborić": 130,
      "Grebaštica": 120,
      "Bilo": 120,
      "Primošten": 130,
      "Rogoznica": 75,
      "Dubrovnik": 360,
      "Dubrovnik Airport (DBV)": 360,
      "Jadrija": 150,
      "Zaton": 150,
      "Marina Zaton": 150,
      "Srima": 150,
      "Vodice": 150,
      "Tribunj": 170,
      "Pirovac": 170,
      "Tisno": 160,
      "Jezera": 170,
      "Murter": 180,
      "Betina": 180,
      "Zadar": 230,
      "Zadar Airport (ZAD)": 210,
      "Tromilja": 140,
      "NP Krka - Lozovac entrance": 145,
      "Lozovac": 145,
      "Skradin - center": 140,
      "NP Krka - Skradin entrance": 140,
      "Marina ACI Skradin": 140,
      "Drniš": 110,
      "NP Krka - Roški Slap entrance": 150,
      "Knin": 140
    },
    "Makarska": {
      "Skradin - center": 210,
      "Šibenik - center": 200,
      "Zadar": 275,
      "Zadar Airport (ZAD)": 275,
      "Zagreb Airport (ZAG)": 610,
      "Novalja": 420
    },
    "Dubrovnik": {
      "Šibenik - center": 485,
      "D-Marin Marina Mandalina Šibenik": 485,
      "Amadria Park Hotel Šibenik": 485,
      "Brodarica - Šibenik": 485,
      "Zablaće": 485,
      "Žaborić": 470,
      "Grebaštica": 460,
      "Bilo": 445,
      "Primošten": 450,
      "Rogoznica": 420,
      "Split Airport (SPU)": 450,
      "Trogir": 420,
      "Split": 360,
      "Jadrija": 490,
      "Zaton": 490,
      "Marina Zaton": 490,
      "Srima": 499,
      "Vodice": 485,
      "Tribunj": 520,
      "Pirovac": 520,
      "Tisno": 495,
      "Jezera": 530,
      "Murter": 535,
      "Betina": 535,
      "Zadar": 625,
      "Zadar Airport (ZAD)": 550,
      "Tromilja": 485,
      "NP Krka - Lozovac entrance": 485,
      "Lozovac": 485,
      "Skradin - center": 485,
      "NP Krka - Skradin entrance": 485,
      "Marina ACI Skradin": 485,
      "Drniš": 450,
      "NP Krka - Roški Slap entrance": 485,
      "Knin": 485
    },
    "Dubrovnik Airport (DBV)": {
      "Šibenik - center": 485,
      "D-Marin Marina Mandalina Šibenik": 485,
      "Amadria Park Hotel Šibenik": 485,
      "Brodarica - Šibenik": 485,
      "Zablaće": 485,
      "Žaborić": 470,
      "Grebaštica": 460,
      "Bilo": 445,
      "Primošten": 450,
      "Rogoznica": 420,
      "Split Airport (SPU)": 450,
      "Trogir": 420,
      "Split": 360,
      "Jadrija": 490,
      "Zaton": 490,
      "Marina Zaton": 490,
      "Srima": 499,
      "Vodice": 485,
      "Tribunj": 520,
      "Pirovac": 520,
      "Tisno": 495,
      "Jezera": 530,
      "Murter": 535,
      "Betina": 535,
      "Zadar": 625,
      "Zadar Airport (ZAD)": 550,
      "Tromilja": 485,
      "NP Krka - Lozovac entrance": 485,
      "Lozovac": 485,
      "Skradin - center": 485,
      "NP Krka - Skradin entrance": 485,
      "Marina ACI Skradin": 485,
      "Drniš": 450,
      "NP Krka - Roški Slap entrance": 485,
      "Knin": 485
    },
    "Jadrija": {
      "Šibenik - center": 30,
      "D-Marin Marina Mandalina Šibenik": 40,
      "Amadria Park Hotel Šibenik": 40,
      "Brodarica - Šibenik": 40,
      "Zablaće": 40,
      "Žaborić": 55,
      "Grebaštica": 65,
      "Bilo": 70,
      "Primošten": 65,
      "Rogoznica": 95,
      "Split Airport (SPU)": 115,
      "Trogir": 115,
      "Split": 150,
      "Dubrovnik": 490,
      "Dubrovnik Airport (DBV)": 490,
      "Vodice": 30,
      "Tribunj": 35,
      "Pirovac": 50,
      "Tisno": 50,
      "Jezera": 55,
      "Murter": 70,
      "Betina": 70,
      "Zadar": 130,
      "Zadar Airport (ZAD)": 125,
      "Tromilja": 65,
      "NP Krka - Lozovac entrance": 70,
      "Lozovac": 70,
      "Skradin - center": 75,
      "NP Krka - Skradin entrance": 75,
      "Marina ACI Skradin": 75,
      "Drniš": 75,
      "NP Krka - Roški Slap entrance": 100,
      "Knin": 105
    },
    "Zaton": {
      "Šibenik - center": 25,
      "D-Marin Marina Mandalina Šibenik": 35,
      "Amadria Park Hotel Šibenik": 35,
      "Brodarica - Šibenik": 40,
      "Zablaće": 35,
      "Žaborić": 50,
      "Grebaštica": 60,
      "Bilo": 65,
      "Primošten": 75,
      "Rogoznica": 90,
      "Split Airport (SPU)": 115,
      "Trogir": 115,
      "Split": 150,
      "Dubrovnik": 490,
      "Dubrovnik Airport (DBV)": 490,
      "Vodice": 30,
      "Tribunj": 35,
      "Pirovac": 50,
      "Tisno": 50,
      "Jezera": 55,
      "Murter": 70,
      "Betina": 70,
      "Zadar": 130,
      "Zadar Airport (ZAD)": 115,
      "Tromilja": 55,
      "NP Krka - Lozovac entrance": 60,
      "Lozovac": 60,
      "Skradin - center": 60,
      "NP Krka - Skradin entrance": 60,
      "Marina ACI Skradin": 60,
      "Drniš": 69,
      "NP Krka - Roški Slap entrance": 75,
      "Knin": 99
    },
    "Marina Zaton": {
      "Šibenik - center": 20,
      "D-Marin Marina Mandalina Šibenik": 30,
      "Amadria Park Hotel Šibenik": 30,
      "Brodarica - Šibenik": 40,
      "Zablaće": 30,
      "Žaborić": 45,
      "Grebaštica": 55,
      "Bilo": 60,
      "Primošten": 70,
      "Rogoznica": 85,
      "Split Airport (SPU)": 115,
      "Trogir": 115,
      "Split": 150,
      "Dubrovnik": 490,
      "Dubrovnik Airport (DBV)": 490,
      "Vodice": 30,
      "Tribunj": 35,
      "Pirovac": 50,
      "Tisno": 50,
      "Jezera": 55,
      "Murter": 70,
      "Betina": 70,
      "Zadar": 130,
      "Zadar Airport (ZAD)": 125,
      "Tromilja": 60,
      "NP Krka - Lozovac entrance": 65,
      "Lozovac": 65,
      "Skradin - center": 55,
      "NP Krka - Skradin entrance": 55,
      "Marina ACI Skradin": 55,
      "Drniš": 69,
      "NP Krka - Roški Slap entrance": 75,
      "Knin": 99
    },
    "Srima": {
      "Šibenik - center": 25,
      "D-Marin Marina Mandalina Šibenik": 30,
      "Amadria Park Hotel Šibenik": 35,
      "Brodarica - Šibenik": 35,
      "Zablaće": 35,
      "Žaborić": 50,
      "Grebaštica": 60,
      "Bilo": 65,
      "Primošten": 75,
      "Rogoznica": 90,
      "Split Airport (SPU)": 115,
      "Trogir": 115,
      "Split": 150,
      "Dubrovnik": 499,
      "Dubrovnik Airport (DBV)": 499,
      "Tribunj": 35,
      "Pirovac": 50,
      "Tisno": 50,
      "Jezera": 50,
      "Murter": 70,
      "Betina": 70,
      "Zadar": 115,
      "Zadar Airport (ZAD)": 110,
      "Tromilja": 50,
      "NP Krka - Lozovac entrance": 55,
      "Lozovac": 55,
      "Skradin - center": 65,
      "NP Krka - Skradin entrance": 65,
      "Marina ACI Skradin": 65,
      "Drniš": 69,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 99
    },
    "Vodice": {
      "Šibenik - center": 30,
      "D-Marin Marina Mandalina Šibenik": 35,
      "Amadria Park Hotel Šibenik": 40,
      "Brodarica - Šibenik": 40,
      "Zablaće": 40,
      "Žaborić": 50,
      "Grebaštica": 55,
      "Bilo": 60,
      "Primošten": 70,
      "Rogoznica": 80,
      "Split Airport (SPU)": 115,
      "Trogir": 115,
      "Split": 150,
      "Dubrovnik": 499,
      "Dubrovnik Airport (DBV)": 499,
      "Jadrija": 30,
      "Zaton": 30,
      "Marina Zaton": 30,
      "Murter": 60,
      "Betina": 60,
      "Zadar": 110,
      "Zadar Airport (ZAD)": 100,
      "Bilice": 35,
      "Tromilja": 50,
      "NP Krka - Lozovac entrance": 60,
      "Lozovac": 60,
      "Skradin - center": 60,
      "NP Krka - Skradin entrance": 60,
      "Marina ACI Skradin": 70,
      "Drniš": 69,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 99,
      "NP Plitvice Lakes": 295,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Tribunj": {
      "Šibenik - center": 40,
      "D-Marin Marina Mandalina Šibenik": 40,
      "Amadria Park Hotel Šibenik": 45,
      "Brodarica - Šibenik": 45,
      "Zablaće": 45,
      "Žaborić": 60,
      "Grebaštica": 75,
      "Bilo": 80,
      "Primošten": 90,
      "Rogoznica": 105,
      "Split Airport (SPU)": 120,
      "Trogir": 120,
      "Split": 170,
      "Dubrovnik": 520,
      "Dubrovnik Airport (DBV)": 520,
      "Jadrija": 35,
      "Zaton": 35,
      "Marina Zaton": 35,
      "Vodice": 35,
      "Murter": 60,
      "Betina": 60,
      "Zadar": 110,
      "Zadar Airport (ZAD)": 100,
      "Tromilja": 65,
      "NP Krka - Lozovac entrance": 70,
      "Lozovac": 70,
      "Skradin - center": 60,
      "NP Krka - Skradin entrance": 60,
      "Marina ACI Skradin": 80,
      "Drniš": 75,
      "NP Krka - Roški Slap entrance": 95,
      "Knin": 105
    },
    "Pirovac": {
      "Šibenik - center": 50,
      "D-Marin Marina Mandalina Šibenik": 50,
      "Amadria Park Hotel Šibenik": 55,
      "Brodarica - Šibenik": 55,
      "Zablaće": 55,
      "Žaborić": 70,
      "Grebaštica": 85,
      "Bilo": 90,
      "Primošten": 100,
      "Rogoznica": 115,
      "Split Airport (SPU)": 125,
      "Trogir": 125,
      "Split": 170,
      "Dubrovnik": 520,
      "Dubrovnik Airport (DBV)": 520,
      "Jadrija": 50,
      "Zaton": 50,
      "Marina Zaton": 50,
      "Srima": 50,
      "Vodice": 50,
      "Zadar": 105,
      "Zadar Airport (ZAD)": 100,
      "Tromilja": 75,
      "NP Krka - Lozovac entrance": 80,
      "Lozovac": 80,
      "Skradin - center": 65,
      "NP Krka - Skradin entrance": 65,
      "Marina ACI Skradin": 50,
      "Drniš": 85,
      "NP Krka - Roški Slap entrance": 85,
      "Knin": 115
    },
    "Tisno": {
      "Šibenik - center": 50,
      "D-Marin Marina Mandalina Šibenik": 55,
      "Amadria Park Hotel Šibenik": 55,
      "Brodarica - Šibenik": 55,
      "Zablaće": 55,
      "Žaborić": 65,
      "Grebaštica": 70,
      "Bilo": 90,
      "Primošten": 80,
      "Rogoznica": 115,
      "Split Airport (SPU)": 130,
      "Trogir": 130,
      "Split": 170,
      "Dubrovnik": 530,
      "Dubrovnik Airport (DBV)": 530,
      "Jadrija": 50,
      "Zaton": 50,
      "Marina Zaton": 50,
      "Srima": 50,
      "Vodice": 50,
      "Zadar": 110,
      "Zadar Airport (ZAD)": 100,
      "Bilice": 50,
      "Tromilja": 75,
      "NP Krka - Lozovac entrance": 80,
      "Lozovac": 80,
      "Skradin - center": 65,
      "NP Krka - Skradin entrance": 65,
      "Marina ACI Skradin": 90,
      "Drniš": 90,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 120,
      "NP Plitvice Lakes": 295,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Jezera": {
      "Šibenik - center": 55,
      "D-Marin Marina Mandalina Šibenik": 60,
      "Amadria Park Hotel Šibenik": 60,
      "Brodarica - Šibenik": 60,
      "Zablaće": 60,
      "Žaborić": 80,
      "Grebaštica": 90,
      "Bilo": 95,
      "Primošten": 105,
      "Rogoznica": 120,
      "Split Airport (SPU)": 135,
      "Trogir": 135,
      "Split": 170,
      "Dubrovnik": 530,
      "Dubrovnik Airport (DBV)": 530,
      "Jadrija": 55,
      "Zaton": 55,
      "Marina Zaton": 55,
      "Srima": 55,
      "Vodice": 55,
      "Zadar": 110,
      "Zadar Airport (ZAD)": 110,
      "Tromilja": 85,
      "NP Krka - Lozovac entrance": 90,
      "Lozovac": 90,
      "Skradin - center": 70,
      "NP Krka - Skradin entrance": 70,
      "Marina ACI Skradin": 90,
      "Drniš": 90,
      "NP Krka - Roški Slap entrance": 95,
      "Knin": 120
    },
    "Murter": {
      "Šibenik - center": 70,
      "D-Marin Marina Mandalina Šibenik": 70,
      "Amadria Park Hotel Šibenik": 80,
      "Brodarica - Šibenik": 80,
      "Zablaće": 80,
      "Žaborić": 95,
      "Grebaštica": 105,
      "Bilo": 110,
      "Primošten": 120,
      "Rogoznica": 135,
      "Split Airport (SPU)": 150,
      "Trogir": 150,
      "Split": 180,
      "Dubrovnik": 535,
      "Dubrovnik Airport (DBV)": 535,
      "Jadrija": 70,
      "Zaton": 70,
      "Marina Zaton": 70,
      "Srima": 70,
      "Vodice": 70,
      "Zadar": 115,
      "Zadar Airport (ZAD)": 115,
      "Tromilja": 95,
      "NP Krka - Lozovac entrance": 100,
      "Lozovac": 100,
      "Skradin - center": 75,
      "NP Krka - Skradin entrance": 75,
      "Marina ACI Skradin": 100,
      "Drniš": 90,
      "NP Krka - Roški Slap entrance": 115,
      "Knin": 120
    },
    "Betina": {
      "Šibenik - center": 70,
      "D-Marin Marina Mandalina Šibenik": 70,
      "Amadria Park Hotel Šibenik": 80,
      "Brodarica - Šibenik": 80,
      "Zablaće": 80,
      "Žaborić": 95,
      "Grebaštica": 105,
      "Bilo": 110,
      "Primošten": 120,
      "Rogoznica": 135,
      "Split Airport (SPU)": 150,
      "Trogir": 150,
      "Split": 180,
      "Dubrovnik": 535,
      "Dubrovnik Airport (DBV)": 535,
      "Jadrija": 70,
      "Zaton": 70,
      "Marina Zaton": 70,
      "Srima": 70,
      "Vodice": 70,
      "Zadar": 115,
      "Zadar Airport (ZAD)": 115,
      "Tromilja": 80,
      "NP Krka - Lozovac entrance": 85,
      "Lozovac": 85,
      "Skradin - center": 75,
      "NP Krka - Skradin entrance": 75,
      "Marina ACI Skradin": 100,
      "Drniš": 90,
      "NP Krka - Roški Slap entrance": 115,
      "Knin": 120
    },
    "Zadar": {
      "Šibenik - center": 140,
      "D-Marin Marina Mandalina Šibenik": 140,
      "Amadria Park Hotel Šibenik": 140,
      "Brodarica - Šibenik": 140,
      "Zablaće": 140,
      "Žaborić": 150,
      "Grebaštica": 155,
      "Bilo": 160,
      "Primošten": 170,
      "Rogoznica": 170,
      "Split Airport (SPU)": 210,
      "Trogir": 210,
      "Split": 230,
      "Dubrovnik": 625,
      "Dubrovnik Airport (DBV)": 625,
      "Jadrija": 140,
      "Zaton": 140,
      "Marina Zaton": 140,
      "Srima": 110,
      "Vodice": 110,
      "Tribunj": 110,
      "Pirovac": 110,
      "Tisno": 110,
      "Jezera": 110,
      "Murter": 130,
      "Betina": 130,
      "Tromilja": 140,
      "NP Krka - Lozovac entrance": 145,
      "Lozovac": 145,
      "Skradin - center": 130,
      "NP Krka - Skradin entrance": 130,
      "Marina ACI Skradin": 130,
      "Drniš": 110,
      "NP Krka - Roški Slap entrance": 135,
      "Knin": 140,
      "NP Plitvice Lakes": 310
    },
    "Novalja": {
      "Šibenik - center": 190,
      "Split": 280,
      "Split Airport (SPU)": 245,
      "Dubrovnik": 680,
      "Dubrovnik Airport (DBV)": 680,
      "Makarska": 420
    },
    "Perković": {
      "Šibenik - center": 55,
      "Skradin - center": 60,
      "Vodice": 70,
      "NP Krka - Lozovac entrance": 60,
      "Split Airport (SPU)": 90,
      "Zadar Airport (ZAD)": 140,
      "Drniš": 95,
      "Knin": 110
    },
    "Zadar Airport (ZAD)": {
      "Šibenik - center": 130,
      "D-Marin Marina Mandalina Šibenik": 130,
      "Amadria Park Hotel Šibenik": 130,
      "Brodarica - Šibenik": 135,
      "Zablaće": 130,
      "Žaborić": 140,
      "Grebaštica": 140,
      "Bilo": 145,
      "Primošten": 160,
      "Rogoznica": 160,
      "Split Airport (SPU)": 200,
      "Trogir": 200,
      "Split": 210,
      "Dubrovnik": 550,
      "Dubrovnik Airport (DBV)": 550,
      "Jadrija": 130,
      "Zaton": 130,
      "Marina Zaton": 130,
      "Srima": 100,
      "Vodice": 100,
      "Tribunj": 100,
      "Pirovac": 100,
      "Tisno": 100,
      "Jezera": 100,
      "Murter": 120,
      "Betina": 120,
      "Bilice": 130,
      "Tromilja": 115,
      "NP Krka - Lozovac entrance": 120,
      "Lozovac": 120,
      "Skradin - center": 105,
      "NP Krka - Skradin entrance": 105,
      "Marina ACI Skradin": 99,
      "Drniš": 110,
      "NP Krka - Roški Slap entrance": 110,
      "Knin": 140,
      "NP Plitvice Lakes": 310,
      "Zagreb": 450,
      "Zagreb Airport (ZAG)": 450
    },
    "Bilice": {
      "Šibenik - center": 20,
      "D-Marin Marina Mandalina Šibenik": 25,
      "Amadria Park Hotel Šibenik": 30,
      "Brodarica - Šibenik": 30,
      "Zablaće": 30,
      "Žaborić": 45,
      "Grebaštica": 55,
      "Bilo": 55,
      "Primošten": 55,
      "Rogoznica": 65,
      "Split Airport (SPU)": 100,
      "Trogir": 115,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 45,
      "Zaton": 45,
      "Marina Zaton": 40,
      "Srima": 45,
      "Vodice": 35,
      "Tribunj": 60,
      "Pirovac": 70,
      "Tisno": 50,
      "Jezera": 75,
      "Murter": 90,
      "Betina": 90,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 130,
      "Tromilja": 35,
      "NP Krka - Lozovac entrance": 40,
      "Lozovac": 40,
      "Skradin - center": 40,
      "NP Krka - Skradin entrance": 40,
      "Marina ACI Skradin": 40,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 80,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Tromilja": {
      "Šibenik - center": 40,
      "D-Marin Marina Mandalina Šibenik": 40,
      "Amadria Park Hotel Šibenik": 40,
      "Brodarica - Šibenik": 50,
      "Žaborić": 50,
      "Grebaštica": 70,
      "Bilo": 75,
      "Primošten": 75,
      "Rogoznica": 90,
      "Split Airport (SPU)": 90,
      "Trogir": 90,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 65,
      "Zaton": 55,
      "Marina Zaton": 60,
      "Srima": 50,
      "Vodice": 50,
      "Tribunj": 65,
      "Pirovac": 75,
      "Tisno": 75,
      "Jezera": 85,
      "Murter": 95,
      "Betina": 80,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 115,
      "Bilice": 35,
      "Skradin - center": 20,
      "NP Krka - Skradin entrance": 20,
      "Marina ACI Skradin": 20,
      "Drniš": 60,
      "NP Krka - Roški Slap entrance": 60,
      "Knin": 90,
      "NP Plitvice Lakes": 305,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "NP Krka - Lozovac entrance": {
      "Šibenik - center": 45,
      "D-Marin Marina Mandalina Šibenik": 45,
      "Amadria Park Hotel Šibenik": 45,
      "Brodarica - Šibenik": 55,
      "Zablaće": 45,
      "Žaborić": 55,
      "Grebaštica": 75,
      "Bilo": 80,
      "Primošten": 80,
      "Rogoznica": 95,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 145,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 70,
      "Zaton": 60,
      "Marina Zaton": 65,
      "Srima": 55,
      "Vodice": 60,
      "Tribunj": 70,
      "Pirovac": 80,
      "Tisno": 80,
      "Jezera": 90,
      "Murter": 100,
      "Betina": 85,
      "Zadar": 145,
      "Zadar Airport (ZAD)": 120,
      "Bilice": 40,
      "Skradin - center": 25,
      "NP Krka - Skradin entrance": 25,
      "Marina ACI Skradin": 25,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 65,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Lozovac": {
      "Šibenik - center": 45,
      "D-Marin Marina Mandalina Šibenik": 45,
      "Amadria Park Hotel Šibenik": 45,
      "Brodarica - Šibenik": 55,
      "Žaborić": 55,
      "Grebaštica": 75,
      "Bilo": 80,
      "Primošten": 80,
      "Rogoznica": 95,
      "Split Airport (SPU)": 95,
      "Trogir": 95,
      "Split": 145,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 70,
      "Zaton": 60,
      "Marina Zaton": 65,
      "Srima": 55,
      "Vodice": 60,
      "Tribunj": 70,
      "Pirovac": 80,
      "Tisno": 80,
      "Jezera": 90,
      "Murter": 100,
      "Betina": 85,
      "Zadar": 145,
      "Zadar Airport (ZAD)": 120,
      "Bilice": 40,
      "Skradin - center": 25,
      "NP Krka - Skradin entrance": 25,
      "Marina ACI Skradin": 25,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 65,
      "Knin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Skradin - center": {
      "Šibenik - center": 50,
      "D-Marin Marina Mandalina Šibenik": 50,
      "Amadria Park Hotel Šibenik": 50,
      "Brodarica - Šibenik": 55,
      "Zablaće": 50,
      "Žaborić": 75,
      "Grebaštica": 80,
      "Bilo": 85,
      "Primošten": 80,
      "Rogoznica": 90,
      "Split Airport (SPU)": 110,
      "Trogir": 100,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 75,
      "Zaton": 60,
      "Marina Zaton": 55,
      "Srima": 65,
      "Vodice": 60,
      "Tribunj": 60,
      "Pirovac": 65,
      "Tisno": 65,
      "Jezera": 70,
      "Murter": 75,
      "Betina": 75,
      "Zadar": 130,
      "Zadar Airport (ZAD)": 105,
      "Bilice": 40,
      "Tromilja": 20,
      "NP Krka - Lozovac entrance": 25,
      "Lozovac": 25,
      "NP Krka - Skradin entrance": 15,
      "Marina ACI Skradin": 15,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 50,
      "Knin": 95,
      "NP Plitvice Lakes": 290,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485,
      "Makarska": 210
    },
    "NP Krka - Skradin entrance": {
      "Šibenik - center": 50,
      "D-Marin Marina Mandalina Šibenik": 50,
      "Amadria Park Hotel Šibenik": 50,
      "Brodarica - Šibenik": 55,
      "Zablaće": 50,
      "Žaborić": 75,
      "Grebaštica": 80,
      "Bilo": 85,
      "Primošten": 80,
      "Rogoznica": 90,
      "Split Airport (SPU)": 110,
      "Trogir": 100,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 75,
      "Zaton": 60,
      "Marina Zaton": 55,
      "Srima": 65,
      "Vodice": 60,
      "Tribunj": 60,
      "Pirovac": 65,
      "Tisno": 65,
      "Jezera": 70,
      "Murter": 75,
      "Betina": 75,
      "Zadar": 130,
      "Zadar Airport (ZAD)": 105,
      "Bilice": 40,
      "Tromilja": 20,
      "NP Krka - Lozovac entrance": 25,
      "Lozovac": 25,
      "Skradin - center": 15,
      "Marina ACI Skradin": 15,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 50,
      "Knin": 95,
      "NP Plitvice Lakes": 290,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Marina ACI Skradin": {
      "Šibenik - center": 50,
      "D-Marin Marina Mandalina Šibenik": 50,
      "Amadria Park Hotel Šibenik": 50,
      "Brodarica - Šibenik": 55,
      "Zablaće": 50,
      "Žaborić": 75,
      "Grebaštica": 80,
      "Bilo": 85,
      "Primošten": 85,
      "Rogoznica": 105,
      "Split Airport (SPU)": 100,
      "Trogir": 95,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 75,
      "Zaton": 60,
      "Marina Zaton": 55,
      "Srima": 65,
      "Vodice": 70,
      "Tribunj": 80,
      "Pirovac": 50,
      "Tisno": 90,
      "Jezera": 90,
      "Murter": 100,
      "Betina": 100,
      "Zadar": 130,
      "Zadar Airport (ZAD)": 100,
      "Bilice": 40,
      "Tromilja": 20,
      "NP Krka - Lozovac entrance": 25,
      "Lozovac": 25,
      "Skradin - center": 15,
      "NP Krka - Skradin entrance": 15,
      "Drniš": 65,
      "NP Krka - Roški Slap entrance": 50,
      "Knin": 95,
      "NP Plitvice Lakes": 290,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Drniš": {
      "Šibenik - center": 65,
      "D-Marin Marina Mandalina Šibenik": 65,
      "Amadria Park Hotel Šibenik": 65,
      "Brodarica - Šibenik": 65,
      "Zablaće": 65,
      "Žaborić": 69,
      "Grebaštica": 69,
      "Bilo": 75,
      "Primošten": 85,
      "Rogoznica": 90,
      "Split Airport (SPU)": 80,
      "Trogir": 80,
      "Split": 110,
      "Dubrovnik": 450,
      "Dubrovnik Airport (DBV)": 450,
      "Jadrija": 75,
      "Zaton": 69,
      "Marina Zaton": 69,
      "Srima": 69,
      "Vodice": 69,
      "Tribunj": 75,
      "Pirovac": 85,
      "Tisno": 90,
      "Jezera": 90,
      "Murter": 90,
      "Betina": 90,
      "Zadar": 110,
      "Zadar Airport (ZAD)": 110,
      "Bilice": 65,
      "Tromilja": 60,
      "NP Krka - Lozovac entrance": 65,
      "Lozovac": 65,
      "Skradin - center": 65,
      "NP Krka - Skradin entrance": 65,
      "Marina ACI Skradin": 65,
      "NP Plitvice Lakes": 310,
      "Zagreb": 450,
      "Zagreb Airport (ZAG)": 450
    },
    "NP Krka - Roški Slap entrance": {
      "Šibenik - center": 90,
      "D-Marin Marina Mandalina Šibenik": 90,
      "Amadria Park Hotel Šibenik": 90,
      "Brodarica - Šibenik": 80,
      "Zablaće": 90,
      "Žaborić": 115,
      "Grebaštica": 90,
      "Bilo": 125,
      "Primošten": 110,
      "Rogoznica": 120,
      "Split Airport (SPU)": 100,
      "Trogir": 110,
      "Split": 150,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 100,
      "Zaton": 75,
      "Marina Zaton": 75,
      "Srima": 90,
      "Vodice": 90,
      "Tribunj": 95,
      "Pirovac": 85,
      "Tisno": 90,
      "Jezera": 95,
      "Murter": 115,
      "Betina": 115,
      "Zadar": 135,
      "Zadar Airport (ZAD)": 110,
      "Bilice": 80,
      "Tromilja": 60,
      "NP Krka - Lozovac entrance": 65,
      "Lozovac": 65,
      "Skradin - center": 50,
      "NP Krka - Skradin entrance": 50,
      "Marina ACI Skradin": 50,
      "NP Plitvice Lakes": 290,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485
    },
    "Knin": {
      "Šibenik - center": 95,
      "D-Marin Marina Mandalina Šibenik": 95,
      "Amadria Park Hotel Šibenik": 95,
      "Brodarica - Šibenik": 95,
      "Zablaće": 95,
      "Žaborić": 99,
      "Grebaštica": 99,
      "Bilo": 105,
      "Primošten": 115,
      "Rogoznica": 120,
      "Split Airport (SPU)": 110,
      "Trogir": 110,
      "Split": 140,
      "Dubrovnik": 485,
      "Dubrovnik Airport (DBV)": 485,
      "Jadrija": 105,
      "Zaton": 99,
      "Marina Zaton": 99,
      "Srima": 99,
      "Vodice": 99,
      "Tribunj": 105,
      "Pirovac": 115,
      "Tisno": 120,
      "Jezera": 120,
      "Murter": 120,
      "Betina": 120,
      "Zadar": 140,
      "Zadar Airport (ZAD)": 140,
      "Bilice": 95,
      "Tromilja": 90,
      "NP Krka - Lozovac entrance": 95,
      "Lozovac": 95,
      "Skradin - center": 95,
      "NP Krka - Skradin entrance": 95,
      "Marina ACI Skradin": 95,
      "NP Plitvice Lakes": 310,
      "Zagreb": 450,
      "Zagreb Airport (ZAG)": 450
    },
    "NP Plitvice Lakes": {
      "Šibenik - center": 310,
      "D-Marin Marina Mandalina Šibenik": 310,
      "Amadria Park Hotel Šibenik": 310,
      "Brodarica - Šibenik": 310,
      "Zablaće": 310,
      "Žaborić": 310,
      "Grebaštica": 320,
      "Bilo": 320,
      "Primošten": 330,
      "Rogoznica": 330,
      "Split Airport (SPU)": 395,
      "Trogir": 395,
      "Split": 420,
      "Dubrovnik": 750,
      "Dubrovnik Airport (DBV)": 750,
      "Jadrija": 310,
      "Zaton": 310,
      "Marina Zaton": 310,
      "Srima": 310,
      "Vodice": 295,
      "Tribunj": 310,
      "Pirovac": 310,
      "Tisno": 295,
      "Jezera": 310,
      "Murter": 310,
      "Betina": 310,
      "Zadar": 310,
      "Zadar Airport (ZAD)": 310,
      "Bilice": 310,
      "Tromilja": 305,
      "NP Krka - Lozovac entrance": 310,
      "Lozovac": 310,
      "Skradin - center": 290,
      "NP Krka - Skradin entrance": 290,
      "Marina ACI Skradin": 290,
      "Drniš": 310,
      "NP Krka - Roški Slap entrance": 290,
      "Knin": 310
    },
    "Zagreb": {
      "Šibenik - center": 485,
      "D-Marin Marina Mandalina Šibenik": 485,
      "Amadria Park Hotel Šibenik": 485,
      "Brodarica - Šibenik": 485,
      "Zablaće": 485,
      "Žaborić": 490,
      "Grebaštica": 495,
      "Bilo": 499,
      "Primošten": 499,
      "Rogoznica": 499,
      "Split Airport (SPU)": 499,
      "Trogir": 499,
      "Split": 520,
      "Dubrovnik": 795,
      "Dubrovnik Airport (DBV)": 795,
      "Jadrija": 485,
      "Zaton": 485,
      "Marina Zaton": 485,
      "Srima": 485,
      "Vodice": 485,
      "Tribunj": 485,
      "Pirovac": 485,
      "Tisno": 485,
      "Jezera": 485,
      "Murter": 485,
      "Betina": 485,
      "Zadar": 450,
      "Zadar Airport (ZAD)": 450,
      "Bilice": 485,
      "Tromilja": 485,
      "NP Krka - Lozovac entrance": 485,
      "Lozovac": 485,
      "Skradin - center": 485,
      "NP Krka - Skradin entrance": 485,
      "Marina ACI Skradin": 485,
      "Drniš": 450,
      "NP Krka - Roški Slap entrance": 485,
      "Knin": 450
    },
    "Zagreb Airport (ZAG)": {
      "Šibenik - center": 485,
      "D-Marin Marina Mandalina Šibenik": 485,
      "Amadria Park Hotel Šibenik": 485,
      "Brodarica - Šibenik": 485,
      "Zablaće": 485,
      "Žaborić": 490,
      "Grebaštica": 495,
      "Bilo": 499,
      "Primošten": 499,
      "Rogoznica": 499,
      "Split Airport (SPU)": 499,
      "Trogir": 499,
      "Split": 520,
      "Dubrovnik": 795,
      "Dubrovnik Airport (DBV)": 795,
      "Jadrija": 485,
      "Zaton": 485,
      "Marina Zaton": 485,
      "Srima": 485,
      "Vodice": 485,
      "Tribunj": 485,
      "Pirovac": 485,
      "Tisno": 485,
      "Jezera": 485,
      "Murter": 485,
      "Betina": 485,
      "Zadar": 450,
      "Zadar Airport (ZAD)": 450,
      "Bilice": 485,
      "Tromilja": 485,
      "NP Krka - Lozovac entrance": 485,
      "Lozovac": 485,
      "Skradin - center": 485,
      "NP Krka - Skradin entrance": 485,
      "Marina ACI Skradin": 485,
      "Drniš": 450,
      "NP Krka - Roški Slap entrance": 485,
      "Knin": 450
    },
    "Seget": {
      "Šibenik - center": 95,
      "Šibenik Bus Station": 95,
      "Šibenik Ferry Port": 95,
      "D-Marin Marina Mandalina Šibenik": 95,
      "Amadria Park Hotel Šibenik": 95,
      "Brodarica - Šibenik": 95,
      "Zablaće": 95,
      "Žaborić": 80,
      "Grebaštica": 80,
      "Bilo": 80,
      "Rogoznica": 30,
      "Dubrovnik": 420,
      "Dubrovnik Airport (DBV)": 420,
      "Jadrija": 115,
      "Zaton": 115,
      "Marina Zaton": 115,
      "Srima": 115,
      "Vodice": 110,
      "Tribunj": 120,
      "Pirovac": 125,
      "Tisno": 130,
      "Jezera": 135,
      "Murter": 150,
      "Betina": 150,
      "Zadar": 210,
      "Zadar Airport (ZAD)": 200,
      "Bilice": 115,
      "Tromilja": 90,
      "NP Krka - Lozovac entrance": 95,
      "Lozovac": 95,
      "Skradin - center": 100,
      "NP Krka - Skradin entrance": 100,
      "Marina ACI Skradin": 94,
      "Drniš": 80,
      "NP Krka - Roški Slap entrance": 110,
      "Knin": 110,
      "NP Plitvice Lakes": 395,
      "Zagreb": 499,
      "Zagreb Airport (ZAG)": 499,
      "D-Resort Hotel Šibenik": 95,
      "Bellevue Superior Hotel Šibenik": 95,
      "Amadria Park Camp": 95
    },
    "Čiovo": {
      "Šibenik - center": 110,
      "Šibenik Bus Station": 110,
      "Šibenik Ferry Port": 110,
      "D-Marin Marina Mandalina Šibenik": 110,
      "Amadria Park Hotel Šibenik": 110,
      "Brodarica - Šibenik": 110,
      "Zablaće": 110,
      "Žaborić": 95,
      "Grebaštica": 95,
      "Bilo": 95,
      "Rogoznica": 45,
      "Dubrovnik": 435,
      "Dubrovnik Airport (DBV)": 435,
      "Jadrija": 130,
      "Zaton": 130,
      "Marina Zaton": 130,
      "Srima": 130,
      "Vodice": 125,
      "Tribunj": 135,
      "Pirovac": 140,
      "Tisno": 145,
      "Jezera": 150,
      "Murter": 165,
      "Betina": 165,
      "Zadar": 225,
      "Zadar Airport (ZAD)": 215,
      "Bilice": 130,
      "Tromilja": 105,
      "NP Krka - Lozovac entrance": 110,
      "Lozovac": 110,
      "Skradin - center": 115,
      "NP Krka - Skradin entrance": 115,
      "Marina ACI Skradin": 109,
      "Drniš": 95,
      "NP Krka - Roški Slap entrance": 125,
      "Knin": 125,
      "NP Plitvice Lakes": 410,
      "Zagreb": 514,
      "Zagreb Airport (ZAG)": 514,
      "D-Resort Hotel Šibenik": 110,
      "Bellevue Superior Hotel Šibenik": 110,
      "Amadria Park Camp": 110
    },
    "ACI Marina Trogir": {
      "Šibenik - center": 110,
      "Šibenik Bus Station": 110,
      "Šibenik Ferry Port": 110,
      "D-Marin Marina Mandalina Šibenik": 110,
      "Amadria Park Hotel Šibenik": 110,
      "Brodarica - Šibenik": 110,
      "Zablaće": 110,
      "Žaborić": 95,
      "Grebaštica": 95,
      "Bilo": 95,
      "Rogoznica": 45,
      "Dubrovnik": 435,
      "Dubrovnik Airport (DBV)": 435,
      "Jadrija": 130,
      "Zaton": 130,
      "Marina Zaton": 130,
      "Srima": 130,
      "Vodice": 125,
      "Tribunj": 135,
      "Pirovac": 140,
      "Tisno": 145,
      "Jezera": 150,
      "Murter": 165,
      "Betina": 165,
      "Zadar": 225,
      "Zadar Airport (ZAD)": 215,
      "Bilice": 130,
      "Tromilja": 105,
      "NP Krka - Lozovac entrance": 110,
      "Lozovac": 110,
      "Skradin - center": 115,
      "NP Krka - Skradin entrance": 115,
      "Marina ACI Skradin": 109,
      "Drniš": 95,
      "NP Krka - Roški Slap entrance": 125,
      "Knin": 125,
      "NP Plitvice Lakes": 410,
      "Zagreb": 514,
      "Zagreb Airport (ZAG)": 514,
      "D-Resort Hotel Šibenik": 110,
      "Bellevue Superior Hotel Šibenik": 110,
      "Amadria Park Camp": 110
    },
    "Marina Trogir (SCT)": {
      "Šibenik - center": 110,
      "Šibenik Bus Station": 110,
      "Šibenik Ferry Port": 110,
      "D-Marin Marina Mandalina Šibenik": 110,
      "Amadria Park Hotel Šibenik": 110,
      "Brodarica - Šibenik": 110,
      "Zablaće": 110,
      "Žaborić": 95,
      "Grebaštica": 95,
      "Bilo": 95,
      "Rogoznica": 45,
      "Dubrovnik": 435,
      "Dubrovnik Airport (DBV)": 435,
      "Jadrija": 130,
      "Zaton": 130,
      "Marina Zaton": 130,
      "Srima": 130,
      "Vodice": 125,
      "Tribunj": 135,
      "Pirovac": 140,
      "Tisno": 145,
      "Jezera": 150,
      "Murter": 165,
      "Betina": 165,
      "Zadar": 225,
      "Zadar Airport (ZAD)": 215,
      "Bilice": 130,
      "Tromilja": 105,
      "NP Krka - Lozovac entrance": 110,
      "Lozovac": 110,
      "Skradin - center": 115,
      "NP Krka - Skradin entrance": 115,
      "Marina ACI Skradin": 109,
      "Drniš": 95,
      "NP Krka - Roški Slap entrance": 125,
      "Knin": 125,
      "NP Plitvice Lakes": 410,
      "Zagreb": 514,
      "Zagreb Airport (ZAG)": 514,
      "D-Resort Hotel Šibenik": 110,
      "Bellevue Superior Hotel Šibenik": 110,
      "Amadria Park Camp": 110
    },
    "Marina Baotić": {
      "Šibenik - center": 95,
      "Šibenik Bus Station": 95,
      "Šibenik Ferry Port": 95,
      "D-Marin Marina Mandalina Šibenik": 95,
      "Amadria Park Hotel Šibenik": 95,
      "Brodarica - Šibenik": 95,
      "Zablaće": 95,
      "Žaborić": 80,
      "Grebaštica": 80,
      "Bilo": 80,
      "Rogoznica": 30,
      "Dubrovnik": 420,
      "Dubrovnik Airport (DBV)": 420,
      "Jadrija": 115,
      "Zaton": 115,
      "Marina Zaton": 115,
      "Srima": 115,
      "Vodice": 110,
      "Tribunj": 120,
      "Pirovac": 125,
      "Tisno": 130,
      "Jezera": 135,
      "Murter": 150,
      "Betina": 150,
      "Zadar": 210,
      "Zadar Airport (ZAD)": 200,
      "Bilice": 115,
      "Tromilja": 90,
      "NP Krka - Lozovac entrance": 95,
      "Lozovac": 95,
      "Skradin - center": 100,
      "NP Krka - Skradin entrance": 100,
      "Marina ACI Skradin": 94,
      "Drniš": 80,
      "NP Krka - Roški Slap entrance": 110,
      "Knin": 110,
      "NP Plitvice Lakes": 395,
      "Zagreb": 499,
      "Zagreb Airport (ZAG)": 499,
      "D-Resort Hotel Šibenik": 95,
      "Bellevue Superior Hotel Šibenik": 95,
      "Amadria Park Camp": 95
    },
    "Marina Agana": {
      "Šibenik - center": 95,
      "Šibenik Bus Station": 95,
      "Šibenik Ferry Port": 95,
      "D-Marin Marina Mandalina Šibenik": 95,
      "Amadria Park Hotel Šibenik": 95,
      "Brodarica - Šibenik": 95,
      "Zablaće": 95,
      "Žaborić": 80,
      "Grebaštica": 80,
      "Bilo": 80,
      "Rogoznica": 30,
      "Dubrovnik": 420,
      "Dubrovnik Airport (DBV)": 420,
      "Jadrija": 115,
      "Zaton": 115,
      "Marina Zaton": 115,
      "Srima": 115,
      "Vodice": 110,
      "Tribunj": 120,
      "Pirovac": 125,
      "Tisno": 130,
      "Jezera": 135,
      "Murter": 150,
      "Betina": 150,
      "Zadar": 210,
      "Zadar Airport (ZAD)": 200,
      "Bilice": 115,
      "Tromilja": 90,
      "NP Krka - Lozovac entrance": 95,
      "Lozovac": 95,
      "Skradin - center": 100,
      "NP Krka - Skradin entrance": 100,
      "Marina ACI Skradin": 94,
      "Drniš": 80,
      "NP Krka - Roški Slap entrance": 110,
      "Knin": 110,
      "NP Plitvice Lakes": 395,
      "Zagreb": 499,
      "Zagreb Airport (ZAG)": 499,
      "D-Resort Hotel Šibenik": 95,
      "Bellevue Superior Hotel Šibenik": 95,
      "Amadria Park Camp": 95
    },
    "Marina Frapa": {
      "Šibenik - center": 65,
      "Šibenik Bus Station": 65,
      "Šibenik Ferry Port": 65,
      "D-Marin Marina Mandalina Šibenik": 65,
      "Amadria Park Hotel Šibenik": 65,
      "Brodarica - Šibenik": 65,
      "Zablaće": 65,
      "Žaborić": 40,
      "Grebaštica": 30,
      "Bilo": 25,
      "Primošten": 15,
      "Split Airport (SPU)": 80,
      "Trogir": 30,
      "Split": 75,
      "Dubrovnik": 420,
      "Dubrovnik Airport (DBV)": 420,
      "Jadrija": 95,
      "Zaton": 90,
      "Marina Zaton": 85,
      "Srima": 90,
      "Vodice": 80,
      "Tribunj": 105,
      "Pirovac": 115,
      "Tisno": 115,
      "Jezera": 120,
      "Murter": 135,
      "Betina": 135,
      "Zadar": 170,
      "Zadar Airport (ZAD)": 160,
      "Bilice": 65,
      "Tromilja": 90,
      "NP Krka - Lozovac entrance": 95,
      "Lozovac": 95,
      "Skradin - center": 90,
      "NP Krka - Skradin entrance": 90,
      "Marina ACI Skradin": 105,
      "Drniš": 90,
      "NP Krka - Roški Slap entrance": 120,
      "Knin": 120,
      "NP Plitvice Lakes": 330,
      "Zagreb": 499,
      "Zagreb Airport (ZAG)": 499,
      "D-Resort Hotel Šibenik": 65,
      "Bellevue Superior Hotel Šibenik": 65,
      "Amadria Park Camp": 65
    },
    "ACI Marina Vodice": {
      "Šibenik - center": 30,
      "Šibenik Bus Station": 30,
      "Šibenik Ferry Port": 30,
      "D-Marin Marina Mandalina Šibenik": 35,
      "Amadria Park Hotel Šibenik": 40,
      "Brodarica - Šibenik": 40,
      "Zablaće": 40,
      "Žaborić": 50,
      "Grebaštica": 55,
      "Bilo": 60,
      "Primošten": 70,
      "Rogoznica": 80,
      "Split Airport (SPU)": 115,
      "Trogir": 115,
      "Split": 150,
      "Dubrovnik": 499,
      "Dubrovnik Airport (DBV)": 499,
      "Jadrija": 30,
      "Zaton": 30,
      "Marina Zaton": 30,
      "Tribunj": 35,
      "Pirovac": 50,
      "Tisno": 50,
      "Jezera": 55,
      "Murter": 60,
      "Betina": 60,
      "Zadar": 110,
      "Zadar Airport (ZAD)": 100,
      "Bilice": 35,
      "Tromilja": 50,
      "NP Krka - Lozovac entrance": 60,
      "Lozovac": 60,
      "Skradin - center": 60,
      "NP Krka - Skradin entrance": 60,
      "Marina ACI Skradin": 70,
      "Drniš": 69,
      "NP Krka - Roški Slap entrance": 90,
      "Knin": 99,
      "NP Plitvice Lakes": 295,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485,
      "D-Resort Hotel Šibenik": 30,
      "Bellevue Superior Hotel Šibenik": 30,
      "Amadria Park Camp": 40,
      "Perković": 70
    },
    "Marina Tribunj": {
      "Šibenik - center": 40,
      "Šibenik Bus Station": 40,
      "Šibenik Ferry Port": 40,
      "D-Marin Marina Mandalina Šibenik": 40,
      "Amadria Park Hotel Šibenik": 45,
      "Brodarica - Šibenik": 45,
      "Zablaće": 45,
      "Žaborić": 60,
      "Grebaštica": 75,
      "Bilo": 80,
      "Primošten": 90,
      "Rogoznica": 105,
      "Split Airport (SPU)": 120,
      "Trogir": 120,
      "Split": 170,
      "Dubrovnik": 520,
      "Dubrovnik Airport (DBV)": 520,
      "Jadrija": 35,
      "Zaton": 35,
      "Marina Zaton": 35,
      "Srima": 35,
      "Vodice": 35,
      "Murter": 60,
      "Betina": 60,
      "Zadar": 110,
      "Zadar Airport (ZAD)": 100,
      "Bilice": 60,
      "Tromilja": 65,
      "NP Krka - Lozovac entrance": 70,
      "Lozovac": 70,
      "Skradin - center": 60,
      "NP Krka - Skradin entrance": 60,
      "Marina ACI Skradin": 80,
      "Drniš": 75,
      "NP Krka - Roški Slap entrance": 95,
      "Knin": 105,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485,
      "D-Resort Hotel Šibenik": 40,
      "Bellevue Superior Hotel Šibenik": 40,
      "Amadria Park Camp": 45
    },
    "Marina Hramina": {
      "Šibenik - center": 70,
      "Šibenik Bus Station": 70,
      "Šibenik Ferry Port": 70,
      "D-Marin Marina Mandalina Šibenik": 70,
      "Amadria Park Hotel Šibenik": 80,
      "Brodarica - Šibenik": 80,
      "Zablaće": 80,
      "Žaborić": 95,
      "Grebaštica": 105,
      "Bilo": 110,
      "Primošten": 120,
      "Rogoznica": 135,
      "Split Airport (SPU)": 150,
      "Trogir": 150,
      "Split": 180,
      "Dubrovnik": 535,
      "Dubrovnik Airport (DBV)": 535,
      "Jadrija": 70,
      "Zaton": 70,
      "Marina Zaton": 70,
      "Srima": 70,
      "Vodice": 70,
      "Tribunj": 60,
      "Zadar": 115,
      "Zadar Airport (ZAD)": 115,
      "Bilice": 90,
      "Tromilja": 95,
      "NP Krka - Lozovac entrance": 100,
      "Lozovac": 100,
      "Skradin - center": 75,
      "NP Krka - Skradin entrance": 75,
      "Marina ACI Skradin": 100,
      "Drniš": 90,
      "NP Krka - Roški Slap entrance": 115,
      "Knin": 120,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485,
      "D-Resort Hotel Šibenik": 70,
      "Bellevue Superior Hotel Šibenik": 70,
      "Amadria Park Camp": 80
    },
    "Marina Betina": {
      "Šibenik - center": 70,
      "Šibenik Bus Station": 70,
      "Šibenik Ferry Port": 70,
      "D-Marin Marina Mandalina Šibenik": 70,
      "Amadria Park Hotel Šibenik": 80,
      "Brodarica - Šibenik": 80,
      "Zablaće": 80,
      "Žaborić": 95,
      "Grebaštica": 105,
      "Bilo": 110,
      "Primošten": 120,
      "Rogoznica": 135,
      "Split Airport (SPU)": 150,
      "Trogir": 150,
      "Split": 180,
      "Dubrovnik": 535,
      "Dubrovnik Airport (DBV)": 535,
      "Jadrija": 70,
      "Zaton": 70,
      "Marina Zaton": 70,
      "Srima": 70,
      "Vodice": 70,
      "Tribunj": 60,
      "Zadar": 115,
      "Zadar Airport (ZAD)": 115,
      "Bilice": 90,
      "Tromilja": 80,
      "NP Krka - Lozovac entrance": 85,
      "Lozovac": 85,
      "Skradin - center": 75,
      "NP Krka - Skradin entrance": 75,
      "Marina ACI Skradin": 100,
      "Drniš": 90,
      "NP Krka - Roški Slap entrance": 115,
      "Knin": 120,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485,
      "D-Resort Hotel Šibenik": 70,
      "Bellevue Superior Hotel Šibenik": 70,
      "Amadria Park Camp": 80
    },
    "ACI Marina Jezera": {
      "Šibenik - center": 55,
      "Šibenik Bus Station": 55,
      "Šibenik Ferry Port": 55,
      "D-Marin Marina Mandalina Šibenik": 60,
      "Amadria Park Hotel Šibenik": 60,
      "Brodarica - Šibenik": 60,
      "Zablaće": 60,
      "Žaborić": 80,
      "Grebaštica": 90,
      "Bilo": 95,
      "Primošten": 105,
      "Rogoznica": 120,
      "Split Airport (SPU)": 135,
      "Trogir": 135,
      "Split": 170,
      "Dubrovnik": 530,
      "Dubrovnik Airport (DBV)": 530,
      "Jadrija": 55,
      "Zaton": 55,
      "Marina Zaton": 55,
      "Srima": 55,
      "Vodice": 55,
      "Zadar": 110,
      "Zadar Airport (ZAD)": 110,
      "Bilice": 75,
      "Tromilja": 85,
      "NP Krka - Lozovac entrance": 90,
      "Lozovac": 90,
      "Skradin - center": 70,
      "NP Krka - Skradin entrance": 70,
      "Marina ACI Skradin": 90,
      "Drniš": 90,
      "NP Krka - Roški Slap entrance": 95,
      "Knin": 120,
      "NP Plitvice Lakes": 310,
      "Zagreb": 485,
      "Zagreb Airport (ZAG)": 485,
      "D-Resort Hotel Šibenik": 55,
      "Bellevue Superior Hotel Šibenik": 55,
      "Amadria Park Camp": 65
    },
    "Marina Kremik": {
      "Šibenik - center": 60,
      "Šibenik Bus Station": 60,
      "Šibenik Ferry Port": 60,
      "D-Marin Marina Mandalina Šibenik": 60,
      "Amadria Park Hotel Šibenik": 60,
      "Brodarica - Šibenik": 60,
      "Zablaće": 60,
      "Žaborić": 40,
      "Grebaštica": 40,
      "Bilo": 35,
      "Split Airport (SPU)": 80,
      "Split": 100,
      "Dubrovnik": 435,
      "Dubrovnik Airport (DBV)": 435,
      "Jadrija": 80,
      "Zaton": 80,
      "Marina Zaton": 80,
      "Srima": 80,
      "Vodice": 75,
      "Tribunj": 100,
      "Pirovac": 110,
      "Tisno": 100,
      "Jezera": 110,
      "Murter": 130,
      "Betina": 130,
      "Zadar": 170,
      "Zadar Airport (ZAD)": 160,
      "Bilice": 60,
      "Tromilja": 80,
      "NP Krka - Lozovac entrance": 90,
      "Lozovac": 90,
      "Skradin - center": 85,
      "NP Krka - Skradin entrance": 85,
      "Marina ACI Skradin": 95,
      "Drniš": 90,
      "NP Krka - Roški Slap entrance": 115,
      "Knin": 120,
      "NP Plitvice Lakes": 330,
      "Zagreb": 500,
      "Zagreb Airport (ZAG)": 500,
      "D-Resort Hotel Šibenik": 60,
      "Bellevue Superior Hotel Šibenik": 60,
      "Amadria Park Camp": 60
    }
  };

  const GROUPS = [
    { label: 'Šibenik area', items: ['Šibenik - center', 'Šibenik Bus Station', 'Šibenik Ferry Port', 'Brodarica - Šibenik', 'Zablaće', 'Bilice', 'Žaborić', 'Jadrija'] },
    { label: 'Airports', items: ['Split Airport (SPU)', 'Zadar Airport (ZAD)', 'Dubrovnik Airport (DBV)', 'Zagreb Airport (ZAG)'] },
    { label: 'Hotels', items: ['Amadria Park Hotel Šibenik', 'Amadria Park Camp', 'D-Resort Hotel Šibenik', 'Bellevue Superior Hotel Šibenik'] },
    { label: 'Marinas', items: ['D-Marin Marina Mandalina Šibenik', 'Marina ACI Skradin', 'Marina Zaton', 'ACI Marina Vodice', 'Marina Tribunj', 'Marina Hramina', 'ACI Marina Jezera', 'Marina Betina', 'Marina Kremik', 'Marina Frapa', 'ACI Marina Trogir', 'Marina Trogir (SCT)', 'Marina Baotić', 'Marina Agana'] },
    { label: 'NP Krka', items: ['NP Krka - Skradin entrance', 'NP Krka - Lozovac entrance', 'NP Krka - Roški Slap entrance'] },
    { label: 'Cities and towns', items: ['Vodice', 'Tribunj', 'Zaton', 'Srima', 'Skradin - center', 'Grebaštica', 'Tisno', 'Murter', 'Betina', 'Jezera', 'Bilo', 'Primošten', 'Rogoznica', 'Pirovac', 'Tromilja', 'Lozovac', 'Drniš', 'Knin', 'Perković', 'Zadar', 'Split', 'Dubrovnik', 'Zagreb', 'Trogir', 'Seget', 'Čiovo', 'Makarska', 'Novalja'] },
    { label: 'Plitvice', items: ['NP Plitvice Lakes'] }
  ];

  // Diacritic-insensitive normalize so "sibenik" matches "Šibenik", etc.
  function normalize(s) {
    return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  }

  // A small type icon next to each combo option: airport, hotel, marina,
  // national park (nature), city, or town (default for populated places).
  const COMBO_CITIES = new Set(['Šibenik - center', 'Split', 'Zadar', 'Dubrovnik', 'Zagreb', 'Trogir', 'Makarska', 'Vodice', 'Skradin - center', 'Drniš', 'Knin', 'Primošten']);
  function iconFor(name) {
    let p;
    if (/Airport/.test(name)) {
      p = '<path d="M21 15.5v-1.4l-7-4.3V5a1.5 1.5 0 0 0-3 0v4.8l-7 4.3v1.4l7-2.1v3.4l-1.9 1.3v1.1L12 18l3.9 1.2v-1.1L14 16.8v-3.4z"/>';
    } else if (/Bus Station/.test(name)) {
      p = '<path d="M5 4h14a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1v1a1 1 0 0 1-2 0v-1H7v1a1 1 0 0 1-2 0v-1a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm1 3v3h5V7H6zm7 0v3h5V7h-5zM7.5 14a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm9 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>';
    } else if (/Hotel|Camp/.test(name)) {
      p = '<path d="M3 19V6a1 1 0 0 1 2 0v5h11a4 4 0 0 1 4 4v4a1 1 0 0 1-2 0v-2H5v2a1 1 0 0 1-2 0zm5-6a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z"/>';
    } else if (name === 'Šibenik Ferry Port' || name === 'NP Krka - Skradin entrance') {
      p = '<path d="M20 21c-1.39 0-2.78-.47-4-1.32-2.44 1.71-5.56 1.71-8 0C6.78 20.53 5.39 21 4 21H2v-2h2c1.38 0 2.74-.35 4-.99 2.52 1.29 5.48 1.29 8 0 1.26.65 2.62.99 4 .99h2v2h-2zM3.95 19H4c1.6 0 3.02-.88 4-2 .98 1.12 2.4 2 4 2s3.02-.88 4-2c.98 1.12 2.4 2 4 2h.05l1.89-6.68c.16-.52-.14-1.06-.66-1.28L20 10.62V6c0-1.1-.9-2-2-2h-3V1H9v3H6c-1.1 0-2 .9-2 2v4.62l-1.28.42c-.52.22-.82.76-.66 1.28L3.95 19zM6 6h12v3.97L12 8 6 9.97z"/>';
    } else if (/Marina/.test(name)) {
      p = '<path d="M3 18h18l-2.2 3H5.2zM12 2 6.5 15H12zM13 6l5.5 9H13z"/>';
    } else if (/^NP /.test(name)) {
      p = '<path d="M12 2 7 11h3l-4 6h5v3h2v-3h5l-4-6h3z"/>';
    } else if (COMBO_CITIES.has(name)) {
      p = '<path d="M3 21V7l5-2.5V7l5-2.5V10h6v11H3zm2.5-3H8v-2H5.5v2zm0-4H8v-2H5.5v2zm0-4H8V8H5.5v2zm7 8H15v-2h-2.5v2zm0-4H15v-2h-2.5v2z"/>';
    } else {
      p = '<path d="M4 21v-9l8-6 8 6v9h-5v-6H9v6z"/>';
    }
    return '<svg class="combo-opt-icon" viewBox="0 0 24 24" width="15" height="15" fill="currentColor" aria-hidden="true">' + p + '</svg>';
  }

  // Searchable, grouped dropdown backed by a hidden input (id kept as
  // quote-from / quote-to so the quote logic can still read .value).
  function initCombo(root) {
    const input = root.querySelector('.combo-input');
    const hidden = root.querySelector('input[type="hidden"]');
    const panel = root.querySelector('.combo-panel');
    const options = [];
    let isOpen = false;
    let activeIdx = -1;

    GROUPS.forEach((group) => {
      const g = document.createElement('div');
      g.className = 'combo-group';
      const gl = document.createElement('div');
      gl.className = 'combo-group-label';
      gl.textContent = group.label;
      g.appendChild(gl);
      group.items.forEach((name) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'combo-option';
        btn.innerHTML = iconFor(name) + '<span class="combo-opt-label"></span>';
        btn.querySelector('.combo-opt-label').textContent = name;
        btn.addEventListener('click', () => choose(name));
        g.appendChild(btn);
        options.push({ el: btn, group: g, value: name, norm: normalize(name) });
      });
      panel.appendChild(g);
    });
    const empty = document.createElement('div');
    empty.className = 'combo-empty';
    empty.textContent = 'No matching location';
    empty.hidden = true;
    panel.appendChild(empty);

    function visible() { return options.filter((o) => !o.el.hidden); }
    function clearActive() { options.forEach((o) => o.el.classList.remove('active')); activeIdx = -1; }
    function setActive(i) {
      const vis = visible();
      if (!vis.length) return;
      activeIdx = (i + vis.length) % vis.length;
      options.forEach((o) => o.el.classList.remove('active'));
      vis[activeIdx].el.classList.add('active');
      vis[activeIdx].el.scrollIntoView({ block: 'nearest' });
    }
    function filter(q) {
      const nq = normalize(q);
      const groupsShown = new Set();
      let any = false;
      options.forEach((o) => {
        const match = nq === '' || o.norm.indexOf(nq) !== -1;
        o.el.hidden = !match;
        if (match) { any = true; groupsShown.add(o.group); }
      });
      panel.querySelectorAll('.combo-group').forEach((g) => { g.hidden = !groupsShown.has(g); });
      empty.hidden = any;
      clearActive();
    }
    function open() {
      if (isOpen) return;
      isOpen = true;
      panel.hidden = false;
      input.setAttribute('aria-expanded', 'true');
      filter('');
    }
    function close() {
      isOpen = false;
      panel.hidden = true;
      input.setAttribute('aria-expanded', 'false');
      input.value = hidden.value;
      clearActive();
    }
    function choose(name) {
      hidden.value = name;
      input.value = name;
      close();
    }

    input.addEventListener('focus', () => { open(); input.select(); });
    input.addEventListener('click', open);
    input.addEventListener('input', () => { open(); filter(input.value); });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') { e.preventDefault(); open(); setActive(activeIdx + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(activeIdx - 1); }
      else if (e.key === 'Enter') {
        if (isOpen) {
          e.preventDefault();
          const vis = visible();
          if (activeIdx >= 0 && vis[activeIdx]) choose(vis[activeIdx].value);
          else if (vis.length === 1) choose(vis[0].value);
        }
      } else if (e.key === 'Escape') { close(); }
    });
    document.addEventListener('click', (e) => { if (!root.contains(e.target)) close(); });
  }

  document.querySelectorAll('#quote-widget .combo').forEach(initCombo);

  const fromSelect = document.getElementById('quote-from');
  const toSelect = document.getElementById('quote-to');

  // Price for one direction; prefers the exact directional value and falls back
  // to the reverse direction when only one is listed. Returns null if the pair
  // has no fixed price (custom quote).
  function priceOneWay(from, to) {
    const f = PRICES[from];
    if (f && f[to] != null) return f[to];
    const r = PRICES[to];
    if (r && r[from] != null) return r[from];
    return null;
  }

  const tripToggleBtns = document.querySelectorAll('.trip-toggle-btn');
  let tripType = 'oneway';
  tripToggleBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      tripToggleBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      tripType = btn.dataset.trip;
    });
  });

  document.querySelectorAll('.stepper-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const target = document.getElementById(btn.dataset.target);
      const delta = parseInt(btn.dataset.delta, 10);
      const min = parseInt(target.dataset.min, 10);
      const max = parseInt(target.dataset.max, 10);
      const next = Math.min(max, Math.max(min, parseInt(target.dataset.value, 10) + delta));
      target.dataset.value = String(next);
      target.textContent = String(next);
    });
  });

  function bookingUrl(q) {
    const params = new URLSearchParams();
    params.set('from', q.from);
    params.set('to', q.to);
    params.set('trip', q.tripType);
    params.set('pax', q.passengers);
    params.set('lug', q.luggage);
    params.set('price', q.priceParam);
    return '/book/?' + params.toString();
  }

  const quoteResult = document.getElementById('quote-result');

  document.getElementById('quote-submit').addEventListener('click', () => {
    const from = fromSelect.value;
    const to = toSelect.value;

    quoteResult.hidden = false;

    if (!from || !to) {
      quoteResult.innerHTML = '<p>Please choose a pickup location and destination.</p>';
      return;
    }

    const passengers = document.getElementById('quote-passengers').dataset.value;
    const luggage = document.getElementById('quote-luggage').dataset.value;
    const base = { from, to, tripType, passengers, luggage };
    const pax = parseInt(passengers, 10);

    // Fixed prices are per car (Škoda Superb, up to 4). Larger groups need a
    // van, so no automatic price: they contact Antonio directly for a quote.
    if (pax >= 9) {
      const url = bookingUrl({ ...base, priceParam: 'custom' });
      quoteResult.innerHTML =
        '<p>For 9 to 12 passengers I put together a van and my car, and drive the car myself. Contact me for a price.</p>' +
        '<a class="btn btn-primary quote-btn" href="' + url + '">Request a Quote</a>';
      return;
    }
    if (pax >= 5) {
      const url = bookingUrl({ ...base, priceParam: 'custom' });
      quoteResult.innerHTML =
        '<p>For 5 to 8 passengers a van is needed. I don\'t run a van myself yet, but contact me and I\'ll do my best to arrange one for you.</p>' +
        '<a class="btn btn-primary quote-btn" href="' + url + '">Request a Quote</a>';
      return;
    }

    if (from === to) {
      const url = bookingUrl({ ...base, priceParam: 'meter' });
      quoteResult.innerHTML =
        '<p>A local ride within ' + from + ' is charged by the taxi meter, from &euro;10. See the <a href="#pricing">local rates</a> below.</p>' +
        '<a class="btn btn-primary quote-btn" href="' + url + '">Book Now</a>';
      return;
    }

    const oneway = priceOneWay(from, to);
    if (oneway != null) {
      let total, sub;
      if (tripType === 'return') {
        total = oneway + priceOneWay(to, from);
        sub = 'return total';
      } else {
        total = oneway;
        sub = 'one way';
      }
      const url = bookingUrl({ ...base, priceParam: String(total) });
      quoteResult.innerHTML =
        '<div class="quote-price">&euro;' + total + ' <span class="quote-price-sub">' + sub + '</span></div>' +
        '<a class="btn btn-primary quote-btn" href="' + url + '">Book Now</a>';
    } else {
      const url = bookingUrl({ ...base, priceParam: 'custom' });
      quoteResult.innerHTML =
        '<p>I don\'t have a listed fixed price for ' + from + ' to ' + to + ' yet, but I\'ll quote you directly.</p>' +
        '<a class="btn btn-primary quote-btn" href="' + url + '">Request a Quote</a>';
    }
  });

  // "Book this" route cards prefill the widget with the route and show the fare.
  // The link's href="#book" handles the scroll up to the form.
  document.querySelectorAll('.ar-book[data-from]').forEach((link) => {
    link.addEventListener('click', () => {
      const set = (hidId, visId, val) => {
        const h = document.getElementById(hidId);
        const v = document.getElementById(visId);
        if (h) h.value = val;
        if (v) v.value = val;
      };
      set('quote-from', 'quote-from-input', link.dataset.from);
      set('quote-to', 'quote-to-input', link.dataset.to);
      document.getElementById('quote-submit').click();
    });
  });

  // Route pages: a [data-prefill-from] marker fills the widget with the route
  // and shows the fixed fare on load, so the visitor lands on a ready quote.
  const prefill = document.querySelector('[data-prefill-from]');
  if (prefill) {
    const set = (hidId, visId, val) => {
      const h = document.getElementById(hidId);
      const v = document.getElementById(visId);
      if (h) h.value = val;
      if (v) v.value = val;
    };
    set('quote-from', 'quote-from-input', prefill.dataset.prefillFrom);
    set('quote-to', 'quote-to-input', prefill.dataset.prefillTo);
    if (prefill.dataset.prefillTrip === 'return') {
      const rb = document.querySelector('.trip-toggle-btn[data-trip="return"]');
      if (rb) rb.click();
    }
    document.getElementById('quote-submit').click();
  }
}

// Booking page: reads the quote from the URL, shows a summary, collects the
// remaining details (date, time, contact) and emails the full request.
const bookingPageForm = document.getElementById('booking-page-form');
if (bookingPageForm) {
  const params = new URLSearchParams(location.search);
  const fromEl = document.getElementById('book-from');
  const toEl = document.getElementById('book-to');
  const tripEl = document.getElementById('book-trip');
  const paxEl = document.getElementById('book-pax');
  const lugEl = document.getElementById('book-lug');
  const priceParam = params.get('price') || '';

  // Prefill the trip fields from the URL (from a route or service-area "Book now").
  if (params.get('from')) fromEl.value = params.get('from');
  if (params.get('to')) toEl.value = params.get('to');
  if (params.get('trip') === 'return') tripEl.value = 'return';
  if (params.get('pax')) paxEl.value = params.get('pax');
  if (params.get('lug')) lugEl.value = params.get('lug');

  // Show the fixed price when we have one.
  let priceText = '';
  if (priceParam === 'meter') priceText = 'Taxi meter (from €10)';
  else if (priceParam && priceParam !== 'custom') priceText = '€' + priceParam;
  if (priceText) {
    document.getElementById('sum-price').textContent = priceText;
    document.getElementById('booking-price-line').hidden = false;
  }

  // Return date/time only when a return trip is chosen.
  const returnFields = document.getElementById('book-return-fields');
  const syncReturn = () => { returnFields.hidden = tripEl.value !== 'return'; };
  tripEl.addEventListener('change', syncReturn);
  syncReturn();

  const bookingPageNote = document.getElementById('booking-page-note');

  // Bookings need at least 2 hours' notice. Block past dates in the picker and
  // enforce the 2-hour minimum on submit.
  const MIN_NOTICE_MS = 2 * 60 * 60 * 1000;
  const todayStr = new Date().toISOString().slice(0, 10);
  const bookDateEl = document.getElementById('book-date');
  const bookReturnDateEl = document.getElementById('book-return-date');
  if (bookDateEl) bookDateEl.min = todayStr;
  if (bookReturnDateEl) bookReturnDateEl.min = todayStr;

  bookingPageForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const from = fromEl.value.trim();
    const to = toEl.value.trim();
    const name = document.getElementById('book-name').value.trim();
    const email = document.getElementById('book-email').value.trim();
    const date = document.getElementById('book-date').value;
    const time = document.getElementById('book-time').value;

    if (!from || !to || !name || !email || !date || !time) {
      bookingPageNote.textContent = 'Please fill in the pickup and drop-off, your name, email, pickup date and time.';
      return;
    }

    const pickupAt = new Date(date + 'T' + time);
    if (isNaN(pickupAt.getTime()) || pickupAt.getTime() - Date.now() < MIN_NOTICE_MS) {
      bookingPageNote.textContent = 'Please choose a pickup at least 2 hours from now. For a sooner ride, call or WhatsApp me directly.';
      return;
    }

    bookingPageNote.textContent = 'Sending...';

    try {
      const body = new FormData();
      body.append('pickup', from);
      body.append('dropoff', to);
      body.append('trip', tripEl.value);
      body.append('pickup_date', date);
      body.append('pickup_time', time);
      body.append('return_date', document.getElementById('book-return-date').value);
      body.append('return_time', document.getElementById('book-return-time').value);
      body.append('passengers', paxEl.value);
      body.append('luggage', lugEl.value);
      body.append('price', priceParam);
      body.append('name', name);
      body.append('email', email);
      body.append('phone', document.getElementById('book-phone').value.trim());
      body.append('flight', document.getElementById('book-flight').value.trim());
      body.append('dropoff_details', document.getElementById('book-dropoff-details').value.trim());
      body.append('notes', document.getElementById('book-notes').value.trim());
      body.append('company', document.getElementById('book-company').value);

      const response = await fetch('/booking-submit.php', {
        method: 'POST',
        body,
        headers: { Accept: 'application/json' }
      });
      const data = await response.json().catch(() => null);

      if (response.ok && data && data.success) {
        bookingPageNote.textContent = 'Thanks! Your booking request has been sent. Antonio will confirm shortly.';
        bookingPageForm.reset();
      } else {
        bookingPageNote.textContent = (data && data.error) || 'Something went wrong. Please call or WhatsApp me instead.';
      }
    } catch (err) {
      bookingPageNote.textContent = 'Something went wrong. Please call or WhatsApp me instead.';
    }
  });
}

const form = document.getElementById('contact-form');
const note = document.getElementById('form-note');

if (form && note) {
  // Pre-fill from URL params, e.g. /contact/?topic=booking&message=...&route=...
  // (used by the header "Book a Transfer" and route-page "Book this route" buttons).
  const cparams = new URLSearchParams(window.location.search);
  const topicParam = cparams.get('topic');
  const messageParam = cparams.get('message');
  const routeParam = cparams.get('route');
  const topicSel = form.querySelector('#topic');
  if (topicParam && topicSel) {
    const opt = Array.from(topicSel.options).find((o) => o.value.toLowerCase() === topicParam.toLowerCase());
    if (opt) topicSel.value = opt.value;
  }
  const msgEl = form.querySelector('#message');
  if (msgEl && !msgEl.value) {
    if (messageParam) {
      msgEl.value = messageParam;
    } else if (routeParam) {
      msgEl.value = 'I would like to book the ' + routeParam + ' transfer. Please confirm availability for my travel date.';
    }
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    note.textContent = 'Sending...';

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      });

      const data = await response.json().catch(() => null);

      if (response.ok && data && data.success) {
        note.textContent = 'Thanks! Your message has been sent. Antonio will get back to you shortly.';
        form.reset();
      } else {
        note.textContent = (data && data.error) || 'Something went wrong. Please call or WhatsApp me instead.';
      }
    } catch (err) {
      note.textContent = 'Something went wrong. Please call or WhatsApp me instead.';
    }
  });
}

// Special offers page: load active empty-leg offers from the PHP feed and render them.
const offersList = document.getElementById('offers-list');
if (offersList) {
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fmtDate = (d) => {
    if (!d) return 'Flexible date';
    const dt = new Date(d + 'T00:00:00');
    return isNaN(dt) ? esc(d) : dt.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' });
  };
  const hm = (t) => (t ? String(t).slice(0, 5) : '');

  fetch('/offers-api.php', { headers: { Accept: 'application/json' } })
    .then((r) => r.json())
    .then((data) => {
      const offers = (data && data.offers) || [];
      if (!offers.length) {
        offersList.innerHTML = '<p class="offers-status">No special offers right now. Check back soon, or <a href="/contact/">contact me</a> for a fixed price on any route.</p>';
        return;
      }
      offersList.innerHTML = offers.map((o) => {
        const price = Math.round(Number(o.price));
        const orig = o.original_price ? Math.round(Number(o.original_price)) : null;
        const dateStr = fmtDate(o.offer_date);
        const win = (o.window_start && o.window_end) ? (hm(o.window_start) + ' - ' + hm(o.window_end)) : '';
        const waMsg = 'Hi Antonio, I would like to grab the special offer: ' + o.route_from + ' to ' + o.route_to +
          ' on ' + dateStr + (win ? ' (' + win + ')' : '') + ' for €' + price + '.\nMy name: \nPassengers: ';
        const wa = 'https://wa.me/385994471013?text=' + encodeURIComponent(waMsg);
        const bookUrl = '/book/?from=' + encodeURIComponent(o.route_from) + '&to=' + encodeURIComponent(o.route_to) +
          '&price=' + price + '&trip=oneway&pax=1&lug=1';
        return '<article class="offer-card">' +
          '<div class="offer-when"><span class="offer-date">' + esc(dateStr) + '</span>' +
          (win ? '<span class="offer-window">' + esc(win) + '</span>' : '') + '</div>' +
          '<div class="offer-route">' + esc(o.route_from) + ' <span>to</span> ' + esc(o.route_to) + '</div>' +
          (o.note ? '<p class="offer-note">' + esc(o.note) + '</p>' : '') +
          '<div class="offer-price">' + (orig ? '<span class="offer-orig">€' + orig + '</span>' : '') +
          '<span class="offer-now">€' + price + '</span>' +
          (o.capacity ? '<span class="offer-seats">up to ' + Number(o.capacity) + '</span>' : '') + '</div>' +
          '<div class="offer-actions">' +
          '<a class="btn btn-primary" href="' + wa + '" target="_blank" rel="noopener">Grab on WhatsApp</a>' +
          '<a class="btn btn-secondary" href="' + bookUrl + '">Book</a>' +
          '</div></article>';
      }).join('');
    })
    .catch(() => {
      offersList.innerHTML = '<p class="offers-status">Could not load offers right now. Please <a href="/contact/">contact me</a> and I\'ll share what\'s available.</p>';
    });
}

// Cookie consent banner + Google Analytics gated behind "Accept".
// Analytics only loads once the visitor accepts; "Reject" leaves it off.
const GA_ID = 'G-XXXXXXXXXX'; // TODO: replace with your GA4 Measurement ID
function loadAnalytics() {
  if (!GA_ID || GA_ID.indexOf('G-XXXX') === 0 || window.__gaLoaded) return;
  window.__gaLoaded = true;
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', GA_ID, { anonymize_ip: true });
}
const cookieBanner = document.getElementById('cookie-banner');
if (cookieBanner) {
  let consent = null;
  try { consent = localStorage.getItem('cookieConsent'); } catch (e) {}
  if (consent === 'accepted') loadAnalytics();
  if (!consent) cookieBanner.hidden = false;
  const setConsent = (value) => {
    try { localStorage.setItem('cookieConsent', value); } catch (e) {}
    cookieBanner.hidden = true;
  };
  const accept = document.getElementById('cookie-accept');
  const reject = document.getElementById('cookie-decline');
  if (accept) accept.addEventListener('click', () => { setConsent('accepted'); loadAnalytics(); });
  if (reject) reject.addEventListener('click', () => setConsent('rejected'));
}
