📖 Sanskrit Sentence Analyzer (Streamlit App)

A simple interactive web app built with Streamlit to analyze Sanskrit sentences using kāraka mappings, dhātu lookup, and vibhakti identification.
This app helps users explore Paninian grammar principles in a modern interface.

🚀 Features

🔍 Sentence Analyzer – Enter a Sanskrit sentence, get word-by-word analysis.

📚 Dhātu Search – Lookup verb roots and their meanings from dhatu_all_combined.txt.

🧩 Kāraka Mapping – Detects kāraka relations from vibhakti and dhātu roots.

🎨 Modern UI – Clean interface with Streamlit (customizable theme).

🛠️ Installation & Setup
1. Clone the Repository
git clone https://github.com/your-username/sanskrit-analyzer.git
cd sanskrit-analyzer

2. Install Dependencies
pip install -r requirements.txt

3. Run the App
streamlit run app.py


The app will open in your browser at http://localhost:8501.

📂 Project Structure
sanskrit-analyzer/
│── app.py                     # Streamlit main app
│── dhatu_search.py            # Dhātu lookup functions
│── karaka_lookup.py           # Kāraka & sūtra mapping
│── shabda_vibhakti.py         # Vibhakti extraction
│── dhatu_all_combined.txt     # Data file for dhātus
│── requirements.txt           # Python dependencies
│── README.md                  # Documentation

🌍 Deployment

You can deploy this app easily on:

Streamlit Cloud (free hosting)

For Streamlit Cloud:

Push your code to GitHub.

Go to share.streamlit.io
.

Select your repo → choose app.py as entry point → Deploy!

✨ Example

Input:

रामः वनम् गच्छति


Output:

रामः → कर्तृ (doer)

वनम् → कर्म (object)

गच्छति → verb (धातु: गम्)

🤝 Contributing

Pull requests are welcome! Please make sure to update tests as appropriate.

📜 License

This project is licensed under the MIT License.
