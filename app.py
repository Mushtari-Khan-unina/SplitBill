import streamlit as st
import pandas as pd

# Function to split the bill and compute additional details
def split_bill(items, participants):
    total_amounts = {person: 0 for person in participants}
    shared_counts = {person: 0 for person in participants}
    individual_counts = {person: 0 for person in participants}
    
    for item in items:
        cost = item['cost']
        shared_by = item['shared_by']
        split_cost = cost / len(shared_by)
        for person in shared_by:
            total_amounts[person] += split_cost
            shared_counts[person] += 1
        if len(shared_by) == 1:
            individual_counts[shared_by[0]] += 1
    
    # Round the total amounts to two decimal places
    total_amounts = {person: round(amount, 2) for person, amount in total_amounts.items()}
    
    return total_amounts, shared_counts, individual_counts

# Main function to run the Streamlit app
def main():
    st.title("Grocery Bill Splitter")
    
    # Step 1: Get participant names
    st.header("Enter Names of Participants")
    num_participants = st.number_input("Number of participants:", min_value=1, step=1)
    
    participants = []
    for i in range(num_participants):
        name = st.text_input(f"Name of participant {i + 1}:", key=f"participant_{i}")
        if name:
            participants.append(name)
    
    if participants:
        st.header("Enter Grocery Items")
        items = []

        # Add item entry form
        num_items = st.number_input("Number of items:", min_value=1, step=1)
        for i in range(num_items):
            with st.expander(f"Item {i + 1}"):
                item_cost = st.number_input(f"Cost of Item {i + 1}:", min_value=0.0, step=0.01, key=f"item_cost_{i}")
                num_shared_by = st.number_input(f"Number of persons sharing Item {i + 1}:", min_value=1, max_value=len(participants), step=1, key=f"num_shared_by_{i}")
                
                if num_shared_by == len(participants):
                    shared_by = participants.copy()
                else:
                    shared_by = []
                    for j in range(num_shared_by):
                        person = st.selectbox(f"Select person {j + 1} sharing Item {i + 1}:", participants, key=f"person_{i}_{j}")
                        if person not in shared_by:
                            shared_by.append(person)
                
                items.append({'cost': item_cost, 'shared_by': shared_by})
        
        if st.button("Calculate"):
            total_amounts, shared_counts, individual_counts = split_bill(items, participants)
            
            st.header("Total Amounts to be Paid")
            result_data = []
            total_bill_sum = 0
            for person in participants:
                total_bill_sum += total_amounts[person]
                result_data.append({
                    'Person Name': person,
                    'No. of Items Shared': shared_counts[person],
                    'No. of Items Individual': individual_counts[person],
                    'Amount': total_amounts[person]
                })
            df = pd.DataFrame(result_data)
            st.table(df)
            
            st.write(f"**Total Bill Sum: ${total_bill_sum:.2f}**")
            
if __name__ == "__main__":
    main()
