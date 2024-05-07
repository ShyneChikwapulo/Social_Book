// Define intents
const intents = [

  {
      tag: "greeting",
      patterns: [
          "hi",
          "hey",
          "how are you",
          "is anyone there?",
          "hello",
          "good day",
          "whats up",
          "ola!",
          "como estas",
          "hey there"
      ],
      responses: [
          "Hey :-)",
          "Hello Vossie, thanks for visiting 👋🏽",
          "Hi there Vossie, what can I do for you?",
          "Hi there Vossie, how can I help?",
          "whats good Playa! 🤙🏽",
          "Whats up buddy "
      ]
  },
  {
      tag: "goodbye",
      patterns: ["bye", "see you later", "goodbye"],
      responses: [
          "See you later, thanks for visiting",
          "Have a nice day",
          "Bye! Come back again soon."
      ]
  },
  {
      tag: "thanks",
      patterns: ["thanks", "thank you", "that's helpful", "thank's a lot!"],
      responses: ["Happy to help!", "Any time!", "My pleasure"]
  },
  {
      tag: "music",
      patterns: [
          "what song are you listening to?",
          "name your favourite song?",
          "what is your favourite song?",
          "what song do you like?"
      ],
      responses: [
          "Clouded by Brent faiyaz",
          "Poison by Brent Faiyaz"
      ]
  },
  {
      tag: "payments",
      patterns: [
          "do you take credit cards?",
          "do you accept mastercard?",
          "can I pay with paypal?",
          "are you cash only?"
      ],
      responses: [
          "We accept VISA, Mastercard and Paypal",
          "We accept most major credit cards, and Paypal"
      ]
  },
  {
      tag: "who",
      patterns: [
          "who are you?",
          "what is your name?",
          "what's your name?",
          "your name is?",
          "name?",
          "introduce yourself"
      ],
      responses: [
          "I am your friend, Vossiebot🤖 but you can call me chrollo",
          "my name is Chrollo your trusty vossiebot🤖",
          "i am vossiebot but they call me chrollo in these streets"
      ]
  },
  {
        tag: "Functions",
        patterns: [
            "app functions?",
            "What do you do?",
            "what can i do here",
        ],
        responses: [
            "Here are the functions of this app:\n1. Share posts\n2. Real-time chat \n3. Find books in Library \n4. Follow friends 5. Like friends post and more"
            
        ]
  },
    {
      tag: "delivery",
      patterns: [
          "how long does delivery take?",
          "how long does shipping take?",
          "when do I get my delivery?"
      ],
      responses: [
          "Delivery takes 2-4 days",
          "Shipping takes 2-4 days"
      ]
    },
  {
    tag: "quotes",
    patterns: [
        "give me a quote",
        "can you give me a quote?",
        "motivate me"
    ],
    responses: [
        "The greatest glory in living lies not in never falling, but in rising every time we fall. -Nelson Mandela",
        "The way to get started is to quit talking and begin doing. -Walt Disney",
        "Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma – which is living with the results of other people's thinking. -Steve Jobs",
        "The future belongs to those who believe in the beauty of their dreams. -Eleanor Roosevelt",
        "If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success. -James Cameron",

    ]
},
  {
      tag: "funny",
      patterns: [
          "tell me a joke!",
          "make jokes",
          "can you make jokes?",
          "tell me something funny",
          "do you know a joke?"
      ],
      responses: [
          "Why did the hipster burn his mouth? He drank the coffee before it was cool.",
          "What did the buffalo say when his son left for college? Bison.",
          "your a joke you silly billy😂",
          "Why didn't the wife attend her husband's funeral? She wasn't much of a mourning person.😂",
          "I went to see my dentist and he warned me it was going to hurt. He ended up telling me he was having an affair with my wife.😓"
      ]
  }
];

// Function to get a response for a given message
function getBotResponse(input) {
    // Normalize message
    const normalizedMessage = input.toLowerCase();

    // Loop through intents
    for (const intent of intents) {
        // Check if any pattern matches the message
        for (const pattern of intent.patterns) {
            if (normalizedMessage.includes(pattern.toLowerCase())) {
                // Randomly select a response
                const responseIndex = Math.floor(Math.random() * intent.responses.length);
                return intent.responses[responseIndex];
            }
        }
    }

    // Default response
    return "I'm sorry, I'm not sure how to respond to that.";
}
