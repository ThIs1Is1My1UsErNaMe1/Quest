import { Configuration, OpenAIApi } from "openai";

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

export default async function (req, res) {
  if (!configuration.apiKey) {
    res.status(500).json({
      error: {
        message: "OpenAI API key not configured, please follow instructions in README.md",
      }
    });
    return;
  }

  const animal = req.body.animal || '';
  if (animal.trim().length === 0) {
    res.status(400).json({
      error: {
        message: "Please enter a valid animal",
      }
    });
    return;
  }

  try {
    const completion = await openai.createCompletion({
      model: "text-davinci-003",
      prompt: generatePrompt(animal),
      temperature: 0.7,
    });
    res.status(200).json({ result: completion.data.choices[0].text });
  } catch(error) {
    // Consider adjusting the error handling logic for your use case
    if (error.response) {
      console.error(error.response.status, error.response.data);
      res.status(error.response.status).json(error.response.data);
    } else {
      console.error(`Error with OpenAI API request: ${error.message}`);
      res.status(500).json({
        error: {
          message: 'An error occurred during your request.',
        }
      });
    }
  }
}

function generatePrompt(animal) {
  const capitalizedAnimal = animal.toLowerCase();
  return `Can you give some IGCSE economics questions about ${capitalizedAnimal}? This is the IGCSE economics syllabus:
  1 The basic economic problem
The first section of the syllabus introduces the fundamental ideas and concepts that underpin the study of
economics including the basic economic problem, factors of production, opportunity cost and production
possibility curves.
2 The allocation of resources
The fundamental principles of resource allocation are considered through the price mechanism in a market
economy. The market forces of demand and supply, market equilibrium and disequilibrium, and elasticity form
the core of this section.
3 Microeconomic decision makers
The microeconomy is an important area of study, and the approach to learning taken here is through the role of
the major decision makers: banks, households, workers, trade unions and firms.
4 Government and the macroeconomy
Governments have different macroeconomic aims, and conflicts often arise between the choice of measures
used to achieve them. Variables must be measured to consider the causes and consequences of change, and
appropriate policies applied.
5 Economic development
As an economy develops there will be changes in population, living standards, poverty and income
redistribution. Therefore, the effects of changes in the size and structure of population and of other influences
on development in a variety of countries are explored.
6 International trade and globalisation
The importance of trade between countries and the growth of globalisation is explored. Principles such as
specialisation, the role of free trade, the role of multinational companies, foreign exchange rates and balance of
payments stability are considered.

Animal: fiscal policy
Names: Discuss whether an increase in taxes will cause deflation [8] 
Discuss whether or not increasing government spending will enable a government to achieve its aims for the economy [8]
Discuss whether or not a reduction in taxes is beneficial for an economy [8]
Animal: monetary policy
Names: Discuss whether a cut in the rate of interest would end deflation [8], 
Discuss whether or not a fall in interest rates will benefit an economy [8], 
Discuss whether or not a central bank should raise the rate of interest [8]
Animal: supply side policy
Names: Discuss whether supply-side policy measures will reduce inflation [8]
Discuss whether or not infrastructure projects will benefit an economy [8] 
Discuss whether or not an economy would benefit from less government regulation [8]
Animal: the role of the government
Names: Discuss whether a government should increase tax rates [8] 
Discuss whether a government should spend more than it raises in taxation [8] 
Discuss whether or not a cut in government spending on education would reduce the gap between government spending and tax revenue [8]
Animal: ${capitalizedAnimal}
Names:`;
}

