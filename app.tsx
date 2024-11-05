// Example function for sending data to the Flask backend
async function runTrain() {
    const response = await fetch('http://localhost:5000/train', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ n_generations: 100, neat_name: 'experiment1' })
    });
    const result = await response.json();
    console.log(result.output); // Process the output as needed
}
