import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.responses import FileResponse
import uvicorn
import nest_asyncio
import asyncio

nest_asyncio.apply()

app = FastAPI()

# Reading the Titanic dataset and analyzing it with FastAPI
@app.post("/analysis")
async def analysis(request: Request):
    df = pd.read_csv('titanic1.csv')
    
    body = await request.json()
    data = body.get('data')

    if data == 'total':
        result = len(df)
        return {"total_records": result}
    elif data == 'female':
        result = df[df['Sex'] == 'female'].shape[0]
        return {"female_count": result}
    elif data == 'male':
        result = df[df['Sex'] == 'male'].shape[0]
        return {"male_count": result}
    elif data == 'female_ratio':
        total_records = len(df)
        female_count = df[df['Sex'] == 'female'].shape[0]
        result = female_count / total_records
        return {"female_ratio": result}
    elif data == 'male_ratio':
        total_records = len(df)
        male_count = df[df['Sex'] == 'male'].shape[0]
        result = male_count / total_records
        return {"male_ratio": result}
    elif data == 'age_below_18':
        result = df[df['Age'] < 18].shape[0]
        return {"age_below_18": result}
    elif data == 'age_18_and_above':
        result = df[df['Age'] >= 18].shape[0]
        return {"age_18_and_above": result}
    elif data == '21':
        result = df[df['Age'] == 21].shape[0]
        return {"age_is_21": result}
    elif data == 'gender_graph':
        female_count = df[df['Sex'] == 'female'].shape[0]
        male_count = df[df['Sex'] == 'male'].shape[0]

        # Create the gender ratio pie chart
        plt.figure(figsize=(6, 6))
        plt.pie([female_count, male_count], labels=['Female', 'Male'], autopct='%1.1f%%', colors=['#ff6666', '#7DF9FF'], startangle=90)
        plt.title('Female and Male Ratio')
        plt.savefig('gender_ratio.png')
        plt.close()

        # Return the chart as a file
        return FileResponse('gender_ratio.png', media_type='image/png')
    else:
        raise HTTPException(status_code=400, detail="Invalid data")

# PUT 
@app.put("/update")
async def update(id: int = Body(...), new_age: float = Body(...)):
    df = pd.read_csv('titanic1.csv')

    if id not in df.index:
        raise HTTPException(status_code=404, detail="Passenger not found")

    
    df.at[id, 'Age'] = new_age
    df.to_csv('titanic1.csv', index=False)
    
    return {"message": f"Passenger ID {id}'s age has been updated to {new_age}"}

# DELETE 
@app.delete("/delete")
async def delete(min: float = Body(...), max: float = Body(...)):
    df = pd.read_csv('titanic1.csv')
    
   
    df_filtered = df[(df['Age'] < min) | (df['Age'] > max)]
    deleted_count = len(df) - len(df_filtered)
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="No passengers found in the specified age range")

    df_filtered.to_csv('titanic1.csv', index=False)
    
    return {"message": f"{deleted_count} passengers between ages {min} and {max} have been deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)